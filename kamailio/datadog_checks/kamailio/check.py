import json
import re
import subprocess
import sys
import traceback
from typing import Callable, Optional

import psutil
import requests

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException, ConfigurationError

from .common import KAMAGENT_RUN_SCRIPT, NAMESPACE, TRACKED_METRICS


class KamailioError(Exception):
    """
    There was an error communicating with Kamailio
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoDispatcherSets(KamailioError):
    """
    No dispatcher sets exist but the module is loaded
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class KamailioCheck(AgentCheck):
    # this will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = NAMESPACE

    def __init__(self, name, init_config, instances):
        super(KamailioCheck, self).__init__(name, init_config, instances)

        # map function defs now to save time during the check execution
        self.TRACKED_METRICS_MAPPING = {k: self._mapMetricSubmissionFunc(v["type"]) for k, v in TRACKED_METRICS.items()}

        # get the instance configs
        self.service_checks = self.instance.get("service_checks", None)
        if self.service_checks is None:
            raise ConfigurationError("Instance Misconfiguration: service_checks is not valid")
        self.jsonrpc_config = self.instance.get("jsonrpc_config", None)
        self.get_modules_from_mmaps = self.instance.get("get_modules_from_mmaps", False)

        # make sure we can communicate with Kamailio
        try:
            self.kamcmd = None  # type: Callable[[str, Optional[tuple|list]], dict|list] | None

            # try JSONRPC first (more accurate results than kamcmd)
            if self.jsonrpc_config is not None:
                try:
                    _ = self._sendJsonRpcCmd("core.version")
                    self.kamcmd = self._sendJsonRpcCmd
                except Exception as ex:
                    self.log.warning("could not communicate with Kamailio via jsonrpc: %s", str(ex))

            # fallback to BINRPC if JSONRPC is not available
            if self.kamcmd is None:
                _ = self._sendBinRpcCmd("core.version")
                self.kamcmd = self._sendBinRpcCmd
        except Exception as ex:
            raise ConfigurationError(f"could not configure kamcmd api: {str(ex)}")

        # make sure we can get the list of Kamailio modules loaded
        # note: reading the modules from memory is only required if kex module is not loaded
        try:
            if self.get_modules_from_mmaps:
                self.kam_modules = KamailioCheck._runKamGetModules()
            else:
                # noinspection PyTypeChecker
                self.kam_modules = self.kamcmd("core.modules")
        except Exception as ex:
            raise ConfigurationError(f"could not find the modules loaded by kamailio: {str(ex)}")

        # exclude tm metrics if tmx module is loaded (tmx metrics will be used instead)
        if "tmx" in self.kam_modules:
            self.TRACKED_METRICS_MAPPING = {k: v for k, v in self.TRACKED_METRICS_MAPPING.items() if k[0:3] != 'tm.'}

    def check(self, instance):
        """
        Run the kamailio service checks and send metrics to datadog API
        """

        # check if configured services are running
        down_services = [service for service in self.service_checks if not KamailioCheck.isProcAlive(service)]
        if len(down_services) != 0:
            self.service_check(
                "services_up", AgentCheck.CRITICAL, message=f"the following services are down: {repr(down_services)}"
            )
            self.log.warning("the following services are down: %s", repr(down_services))
            return

        self.service_check("services_up", AgentCheck.OK)
        self.log.debug("all services are up")

        # gather and send metrics
        try:
            # get main list of statistics if kex module is loaded
            if "kex" in self.kam_modules:
                regex = re.compile(r":| = ")

                # filter non-tracked stats and format data for submission
                for stat in self.kamcmd("stats.get_statistics", ["all"]):
                    tmp = re.split(regex, stat)
                    try:
                        submitMetric = self.TRACKED_METRICS_MAPPING[f"{tmp[0]}.{tmp[1]}"]
                    except KeyError:
                        continue
                    submitMetric(f"{tmp[0]}.{tmp[1]}", float(tmp[2]))

                # get pkg memory stats
                if (
                    'pkg.free' in self.TRACKED_METRICS_MAPPING
                    and 'pkg.real_used' in self.TRACKED_METRICS_MAPPING
                    and 'pkg.total_size' in self.TRACKED_METRICS_MAPPING
                ):
                    pkg_info = self.kamcmd("pkg.stats")
                    for i in range(len(pkg_info)):
                        self.TRACKED_METRICS_MAPPING['pkg.free'](
                            'pkg.free', float(pkg_info[i]['free']), tags=[f"proc:{i}"]
                        )
                        self.TRACKED_METRICS_MAPPING['pkg.real_used'](
                            'pkg.real_used', float(pkg_info[i]['real_used']), tags=[f"proc:{i}"]
                        )
                        self.TRACKED_METRICS_MAPPING['pkg.total_size'](
                            'pkg.total_size', float(pkg_info[i]['total_size']), tags=[f"proc:{i}"]
                        )

            # get extra tcp info
            tcp_info = self.kamcmd("core.tcp_info")
            if 'tcp.max_connections' in self.TRACKED_METRICS_MAPPING:
                self.TRACKED_METRICS_MAPPING["tcp.max_connections"](
                    "tcp.max_connections", float(tcp_info['max_connections'])
                )

            # get stats about dispatcher sets if module is loaded
            if "dispatcher" in self.kam_modules:
                num_destinations = 0.0
                active_destinations = 0.0
                inactive_destinations = 0.0
                trying_destinations = 0.0
                disabled_destinations = 0.0
                estimated_latencies = {}

                # get data and handle case where there are no dispatcher sets
                try:
                    data = self.kamcmd("dispatcher.list")

                    for i in range(data["NRSETS"]):
                        for j in range(len(data["RECORDS"][i]['SET']["TARGETS"])):
                            dest = data['RECORDS'][i]['SET']['TARGETS'][j]['DEST']
                            num_destinations += 1

                            if dest["FLAGS"][0] == "A":
                                active_destinations += 1
                            elif dest["FLAGS"][0] == "I":
                                inactive_destinations += 1
                            elif dest["FLAGS"][0] == "T":
                                trying_destinations += 1
                            elif dest["FLAGS"][0] == "D":
                                disabled_destinations += 1

                            # latency stats only available if ds_ping_latency_stats is enabled
                            try:
                                estimated_latencies[dest["URI"]] = dest["LATENCY"]["EST"]
                            except KeyError:
                                self.log.warning(
                                    "dispatcher parameter ds_ping_latency_stats not enabled, latency stats available"
                                )

                    # if len(estimated_latencies) > 0:
                    #     estimated_latencies["avg"] = sum(estimated_latencies.values()) / len(estimated_latencies)
                    # else:
                    #     estimated_latencies["avg"] = 0.0
                except NoDispatcherSets:
                    self.log.warning("no dispatcher record sets found")

                # filter out untracked metrics and submit data
                if "dispatcher.destinations" in self.TRACKED_METRICS_MAPPING:
                    self.TRACKED_METRICS_MAPPING["dispatcher.destinations"]("dispatcher.destinations", num_destinations)
                if "dispatcher.active" in self.TRACKED_METRICS_MAPPING:
                    self.TRACKED_METRICS_MAPPING["dispatcher.active"]("dispatcher.active", active_destinations)
                if "dispatcher.inactive" in self.TRACKED_METRICS_MAPPING:
                    self.TRACKED_METRICS_MAPPING["dispatcher.inactive"]("dispatcher.inactive", inactive_destinations)
                if "dispatcher.trying" in self.TRACKED_METRICS_MAPPING:
                    self.TRACKED_METRICS_MAPPING["dispatcher.trying"]("dispatcher.trying", trying_destinations)
                if "dispatcher.disabled" in self.TRACKED_METRICS_MAPPING:
                    self.TRACKED_METRICS_MAPPING["dispatcher.disabled"]("dispatcher.disabled", disabled_destinations)
                if "dispatcher.latency" in self.TRACKED_METRICS_MAPPING:
                    for dest_uri, latency in estimated_latencies.items():
                        self.TRACKED_METRICS_MAPPING["dispatcher.latency"](
                            "dispatcher.latency", latency, tags=[f"dest:{dest_uri}"]
                        )

            # get stats from tm module instead (if tmx module is loaded these stats will be excluded)
            if "tm" in self.kam_modules:
                for stat, value in self.kamcmd("tm.stats").items():
                    # filter non-tracked stats and submit data
                    try:
                        submitMetric = self.TRACKED_METRICS_MAPPING[f"tm.{stat}"]
                    except KeyError:
                        continue
                    submitMetric(f"tm.{stat}", float(value))

        except Exception as ex:
            self.log.error("unhandled error occurred while retrieving statistics: %s", str(ex))
            self.logBackTrace()
            return

        self.log.debug("successfully submitted kamailio metrics")

    @staticmethod
    def isProcAlive(name):
        """
        Check if a process is running.

        :param name:    Process name to check
        :type name:     str
        :return:        Whether the process is running or not
        :rtype:         bool
        """

        return any(proc.info["name"] == name for proc in psutil.process_iter(["name"]))

    def _mapMetricSubmissionFunc(self, name):
        if name == "monotonic_count":
            return self.monotonic_count
        elif name == "count":
            return self.count
        elif name == "gauge":
            return self.gauge
        elif name == "rate":
            return self.rate
        elif name == "histogram":
            return self.histogram
        elif name == "historate":
            return self.historate
        elif name == "increment":
            return self.increment
        elif name == "decrement":
            return self.decrement
        else:
            raise CheckException(f'metric type "{name}" is not supported')

    @staticmethod
    def handleDuplicateKeysHook(kv_tuples):
        keys = [kv[0] for kv in kv_tuples]
        if len(keys) == len(set(keys)):
            return {k: v for k, v in kv_tuples}
        return [{k: v} for k, v in kv_tuples]

    def _sendJsonRpcCmd(self, method, params=()):
        """
        Send a JSONRPC command to Kamailio

        :param method:    method as parsed by `kamcmd <https://github.com/kamailio/kamailio/tree/master/utils/kamcmd>`_
        :type method:     str
        :param params:    parameters for the command
        :type params:     tuple|list
        :return:          The result from Kamailio
        :rtype:           dict|list
        :raises requests.exceptions.HTTPError:          if an HTTP error occurred
        :raises requests.exceptions.JSONDecodeError:    if a JSON parsing error occurred
        :raises KamailioError:                          if communicating with Kamailio failed
        :raises Exception:                              for any other error
        """

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if len(self.jsonrpc_config.get("token", "")) > 0:
            headers["Authorization"] = f'Bearer {self.jsonrpc_config["token"]}'

        r = requests.post(
            self.jsonrpc_config["url"],
            headers=headers,
            json={
                "method": method,
                "jsonrpc": self.jsonrpc_config["version"],
                "id": self.jsonrpc_config["id"],
                "params": params,
            },
            verify=self.jsonrpc_config["verify_ssl"],
            allow_redirects=self.jsonrpc_config["allow_redirects"],
            timeout=5,
        )
        r.raise_for_status()

        data = r.json()
        if "error" in data:
            # specific cases
            if data["error"] == "No Destination Sets":
                raise NoDispatcherSets(data["error"])
            # general case
            raise KamailioError(data["error"])

        return data["result"]

    def _sendBinRpcCmd(self, method, params=()):
        """
        Send a BINRPC command to Kamailio

        :param method:  method as parsed by `kamcmd <https://github.com/kamailio/kamailio/tree/master/utils/kamcmd>`_
        :type method:   str
        :param params:  parameters for the command
        :type params:   tuple|list
        :return:        The result from Kamailio
        :rtype:         dict|list
        :raises KamailioError:  if communicating with Kamailio failed
        :raises Exception:      for any other error
        """

        p = subprocess.Popen(
            [KAMAGENT_RUN_SCRIPT, 'kamcmd', method, *params],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        res = p.communicate()

        if len(res[1]) > 0:
            err = res[1].decode("utf-8").strip()
            if err[:6] == 'error:':
                raise KamailioError(err.split(" - ")[1])
            else:
                raise Exception(err)

        # format data as real JSON
        data = res[0].decode("utf-8")
        if data[0] == "{":
            data = re.sub(
                # add brackets for list of objects
                r"((?:\{.*\},)+[ \t\n]*{.*\})[ \t\n]*",
                r"[\1]",
                # remove last comma from lists/dists
                re.sub(
                    r"([\}\]])(?![ |\t|\n]+(?:[\}\]]|$))",
                    r"\1,",
                    # remove last comma from fields
                    re.sub(
                        r'([ |\t|\n]+"[a-zA-Z0-9._-]+": )(?!\{\n|\[\n)([^\n,]+),(\n)(?=[ |\t|\n]*(?:\}|\]))',
                        r"\1\2\3",
                        # fix unquoted list/dict identifiers
                        re.sub(
                            r"([ |\t|\n]+)([a-zA-Z0-9._-]+?): ([\{\[])\n",
                            r'\1"\2": \3\n',
                            # fix unquoted integers and their identifiers and add comma
                            re.sub(
                                r"([ |\t|\n]+)([a-zA-Z0-9._-]+?): ([0-9.-]+)\n",
                                r'\1"\2": \3,\n',
                                # replace incorrect null string with correct null for JSON
                                re.sub(
                                    r'"\<null string\>"',
                                    "null",
                                    # fix unquoted strings and their identifiers and add comma
                                    re.sub(
                                        r"([ |\t|\n]+)([a-zA-Z0-9._-]+?): (?!\{\n|\[\n|[0-9.-]+\n)(.+?)\n",
                                        r'\1"\2": "\3",\n',
                                        data,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                flags=re.DOTALL,
            )

            # parse the json data
            data = json.loads(data, object_pairs_hook=KamailioCheck.handleDuplicateKeysHook)

            # handle edge cases not handled by duplicate key hook
            # the goal is to have output equivalent to the JSONRPC version
            if method == 'dispatcher.list':
                n = data["NRSETS"]
                if n == 1:
                    data['RECORDS'] = [data['RECORDS']]
                if isinstance(data['RECORDS'][0]['SET']['TARGETS'], dict):
                    data['RECORDS'][0]['SET']['TARGETS'] = [data['RECORDS'][0]['SET']['TARGETS']]

            return data

        # return the data as a list
        return data.strip().split("\n")

    @staticmethod
    def _runKamGetModules():
        """
        Run the kamgetmodules command

        :return:                The result from the command
        :rtype:                 list
        :raises KamailioError:  if communicating with Kamailio failed
        :raises Exception:      for any other error
        """

        p = subprocess.Popen(
            [KAMAGENT_RUN_SCRIPT, 'getmodules'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        res = p.communicate()

        if len(res[1]) > 0:
            err = res[1].decode("utf-8").strip()
            if err[:6] == 'error:':
                raise KamailioError(err.split(" - ")[1])
            else:
                raise Exception(err)

        return res[0].decode("utf-8").strip().split()

    def logBackTrace(self):
        # get basic info and the stack
        exc_type, exc_value, exc_tb = sys.exc_info()
        text = "((( EXCEPTION )))\n[CLASS]: {}\n[VALUE]: {}\n".format(exc_type, exc_value)
        tb_list = traceback.extract_tb(exc_tb)

        # ensure a backtrace exists first
        if tb_list is not None and len(tb_list) > 0:
            text += "((( BACKTRACE )))\n"

            for tb_info in tb_list:
                filename, linenum, funcname, source = tb_info

                if funcname != '<module>':
                    funcname = funcname + '()'
                text += "[FILE]: {}\n[LINE NUM]: {}\n[FUNCTION]: {}\n[SOURCE]: {}\n".format(
                    filename, linenum, funcname, source
                )

        self.log.error(text)
