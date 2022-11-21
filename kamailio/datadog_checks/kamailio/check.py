import json
import re
import subprocess

import psutil

from datadog_checks.base import AgentCheck


class KamailioCheck(AgentCheck):
    # this will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'kamailio'

    def __init__(self, name, init_config, instances):
        super(KamailioCheck, self).__init__(name, init_config, instances)

    def check(self, instance):
        """
        Run the kamailio service checks and send metrics to datadog API

        :param instance:    The current instance configuration
        :type instance:     object|dict
        :return:            None
        :rtype:             None
        """

        # validate instance configs
        jsonrpc_api_url = instance.get('jsonrpc_api_url')
        if jsonrpc_api_url is None:
            self.service_check(
                "services_up", AgentCheck.WARNING, message='agent misconfiguration: jsonrpc_api_url is not valid'
            )
            return None

        # check if kamailio process is alive
        if not KamailioCheck.isProcAlive('kamailio'):
            self.service_check("services_up", AgentCheck.CRITICAL, message='kamailio service is down')
            return None

        self.service_check("services_up", AgentCheck.OK, message='kamailio service is up')

        # gather and send metrics
        try:
            r = self.http.post(
                jsonrpc_api_url,
                headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                data=json.dumps({"method": "stats.get_statistics", "jsonrpc": "2.0", "id": 1, "params": ["all"]}),
            )
            r.raise_for_status()

            data = r.json()
            if 'error' in data:
                self.log.warning('can not retrieve stats via jsonrpc: %s', {data["error"]})
                raise Exception()

            data = data['result']
            regex = re.compile(r':| = ')
            for stat in data:
                tmp = re.split(regex, stat)
                name = f'{tmp[0]}.{tmp[1]}'.replace('-', '_')
                self.gauge(name, float(tmp[2]))
        except Exception:
            try:
                p = subprocess.Popen(['kamcmd', '-f', '#%v\n', 'stats.get_statistics', 'all'], stdout=subprocess.PIPE)
                data = p.communicate()[0].decode('utf-8')

                if data[0] != '#':
                    self.log.warning('can not retrieve stats via kamcmd: %s', {data[0]})
                    raise Exception()
                else:
                    regex = re.compile(r'#(.*):(.*) = ([0-9]+)')
                    for stat in re.finditer(regex, data):
                        self.gauge(f'{stat.group(1)}.{stat.group(2)}', float(stat.group(3)))
            except Exception:
                self.service_check(
                    "metrics_up", AgentCheck.WARNING, message='could not retrieve statistics from kamailio'
                )
                return None

        self.service_check("metrics_up", AgentCheck.OK, message='kamailio metrics submitted')

    @staticmethod
    def isProcAlive(name):
        """
        Check if a process is running.

        :param name:    Process name to check
        :type name:     str
        :return:        Whether the process is running or not
        :rtype:         bool
        """

        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == name:
                return True
        return False
