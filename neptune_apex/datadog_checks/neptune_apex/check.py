import datetime
from typing import Any
from xml.etree import ElementTree as ET

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError

# from datadog_checks.base.utils.db import QueryManager
# from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
# from json import JSONDecodeError


class NeptuneApexCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = "neptune_apex"

    def __init__(self, name, init_config, instances):
        super(NeptuneApexCheck, self).__init__(name, init_config, instances)
        self.tags = self.instance.get("tags", [])
        self.address = self.instance.get("address")
        if not self.address:
            raise ConfigurationError("missing required address field")
        self.address = self.address.rstrip("/")

    def check(self, _):
        # type: (Any) -> None
        self.collect_status()
        self.collect_outlog()

    def collect_status(self):
        # these apis tend to leave prepended and dangling empty space, yuck, so you'll see a lot of .strip()
        url = "{}/cgi-bin/status.xml".format(self.address)
        try:
            response = self.http.get(url)
            response.raise_for_status()
            data = ET.fromstring(response.text)
            status = next(data.iter("status"))
            # collect tags
            base_tags = self.tags.copy()
            base_tags.extend(["controller_{}:{}".format(k.strip(), v.strip()) for k, v in status.attrib.items()])

            controller_name = data.find("hostname").text.strip()
            base_tags.append("controller_name:{}".format(controller_name))

            serial = data.find("serial").text.strip()
            base_tags.append("controller_serial:{}".format(serial))

            # iterate over probes, collect first because we need them for outlets
            probes_by_name = {}
            for probe in status.find("probes").iter("probe"):
                probe_name = probe.find("name").text.strip()
                probe_value = float(probe.find("value").text.strip())
                probe_type = probe.find("type")
                if not probe_type:
                    probe_type = "unknown"
                    # try to infer probe type by name, these are defaults for installs.
                    for hint in [
                        "lls",
                        "light",
                        "retpump",
                        "heater",
                        "fan",
                        "skimmer",
                        "reflight",
                        "volt",
                        "orp",
                        "ph",
                        "temp",
                    ]:
                        if hint in probe_name.lower():
                            probe_type = hint
                else:
                    probe_type = probe_type.text.strip().lower()
                probe_tags = base_tags + ["probe_name:{}".format(probe_name)]
                probes_by_name[probe_name] = {
                    "value": probe_value,
                    "type": probe_type,
                    "tags": probe_tags,
                }

            # iterate over outlets
            for outlet in status.find("outlets").iter("outlet"):
                outlet_name = outlet.find("name").text.strip()
                outlet_id = outlet.find("outputID").text.strip()
                outlet_state = outlet.find("state").text.strip()  # this is the configuration state
                outlet_device_id = outlet.find("deviceID").text.strip()
                xstatus = outlet.find("xstatus")
                if not xstatus:
                    xstatus = ""
                else:
                    xstatus = xstatus.text.strip()

                tags = base_tags + [
                    "name:{}".format(outlet_name),
                    "id:{}".format(outlet_id),
                    "state:{}".format(outlet_state),
                    "device_id:{}".format(outlet_device_id),
                ]
                if xstatus:
                    tags.append("status:{}".format(xstatus))

                outlet_watts = None
                # find outlet watts & amps - this comes from the probes and
                # append a "W" or "A" respectively
                probe_watts_name = "{}W".format(outlet_name)
                probe_watts = probes_by_name.get(probe_watts_name, None)
                if probe_watts:
                    del probes_by_name[probe_watts_name]
                    outlet_watts = probe_watts["value"]

                outlet_amps = None
                probe_amps_name = "{}A".format(outlet_name)
                probe_amps = probes_by_name.get(probe_amps_name, None)
                if probe_amps:
                    del probes_by_name[probe_amps_name]
                    outlet_amps = probe_amps["value"]

                # determine outlet type
                outlet_type = "unknown"
                if outlet_device_id.startswith("base_Var"):
                    outlet_type = "variable"
                elif outlet_device_id in ["base_Alarm", "base_Warn"]:
                    outlet_type = "alert"
                elif outlet_device_id.startswith("base_email"):
                    outlet_type = "alert"
                elif outlet_watts is not None or outlet_amps is not None:
                    outlet_type = "outlet"
                elif outlet_device_id.startswith("Cntl_"):
                    outlet_type = "virtual"

                tags.append("outlet_type:{}".format(outlet_type))

                # report state then usage
                outlet_state = -1 # unknown
                if outlet_watts is not None:
                    outlet_state = 0
                    if outlet_watts > 0:
                        outlet_state = 1
                self.count("outlet.state", outlet_state, tags=tags)
                if outlet_watts is not None:
                    self.gauge("outlet.usage.watts", outlet_watts, tags=tags)
                if outlet_amps is not None:
                    self.gauge("outlet.usage.amps", outlet_amps, tags=tags)

            # now report remaining probes
            for probe in probes_by_name.values():
                self.gauge("probe.{}".format(probe["type"]), probe["value"], tags=probe["tags"])

            self.service_check("can_connect", AgentCheck.OK, tags=base_tags + ["collection:status"])
            self.count("can_connect", 1, tags=base_tags + ["collection:status"])
        except Timeout as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self.tags + ["collection:status"],
                message="Request timeout: {}, {}".format(self.address, e),
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:status"])
            raise
        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self.tags + ["collection:status"],
                message="Request failed: {}, {}".format(self.address, e),
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:status"])
            raise

        except ET.ParseError as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self.tags + ["collection:status"],
                message="XML Parse failed: {}, {}".format(self.address, e),
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:status"])
            raise

        except Exception as e:
            self.service_check(
                "can_connect", AgentCheck.CRITICAL, tags=self.tags + ["collection:status"], message=str(e)
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:status"])
            raise

    def collect_outlog(self):
        # This is how you use the persistent cache. This cache file based and persists across agent restarts.
        # If you need an in-memory cache that is persisted across runs
        # You can define a dictionary in the __init__ method.
        # self.write_persistent_cache("key", "value")
        # value = self.read_persistent_cache("key")
        # these apis tend to leave prepended and dangling empty space, yuck, so you'll see a lot of .strip()
        address_hash = abs(hash(self.address)) % (10**8)
        last_log_timestamp_key = "neptune_apex_{}_ts".format(address_hash)
        last_ts = self.read_persistent_cache(last_log_timestamp_key)
        last_recorded_date = datetime.datetime.fromtimestamp(0)
        if last_ts:
            last_recorded_date = datetime.datetime.fromtimestamp(float(last_ts))

        url = "{}/cgi-bin/outlog.xml".format(self.address)
        try:
            response = self.http.get(url)
            response.raise_for_status()
            data = ET.fromstring(response.text)
            outlog = next(data.iter("outlog"))

            # collect tags
            base_tags = self.tags.copy()
            base_tags.extend(["controller_{}:{}".format(k.strip(), v.strip()) for k, v in outlog.attrib.items()])

            controller_name = data.find("hostname").text.strip()
            base_tags.append("controller_name:{}".format(controller_name))

            serial = data.find("serial").text.strip()
            base_tags.append("controller_serial:{}".format(serial))

            for record in outlog.iter("record"):
                date = record.find("date").text.strip()
                name = record.find("name").text.strip()
                value = record.find("value").text.strip()
                try:
                    date = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
                except ValueError:
                    # failure to parse, skip
                    continue

                if date > last_recorded_date:
                    ts = datetime.datetime.timestamp(date)
                    self.event(
                        {
                            "timestamp": ts,
                            "msg_title": "Outlet {} was turned {} on {} ({})".format(
                                name, value, controller_name, serial
                            ),
                            "msg_text": "Outlet state was toggled for {} on {} ({}). Turned to {}.".format(
                                name, controller_name, serial, value
                            ),
                            "tags": base_tags + ["source:neptune_apex"],
                            "source_type_name": "neptune_apex",
                        }
                    )
                    self.write_persistent_cache(last_log_timestamp_key, str(ts))
            self.service_check("can_connect", AgentCheck.OK, tags=base_tags + ["collection:outlog"])
            self.count("can_connect", 1, tags=base_tags + ["collection:outlog"])
        except Timeout as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self.tags + ["collection:outlog"],
                message="Request timeout: {}, {}".format(self.address, e),
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:outlog"])
            raise
        except (HTTPError, InvalidURL, ConnectionError) as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self.tags + ["collection:outlog"],
                message="Request failed: {}, {}".format(self.address, e),
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:outlog"])
            raise

        except ET.ParseError as e:
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self.tags + ["collection:outlog"],
                message="XML Parse failed: {}, {}".format(self.address, e),
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:outlog"])
            raise

        except Exception as e:
            self.service_check(
                "can_connect", AgentCheck.CRITICAL, tags=self.tags + ["collection:outlog"], message=str(e)
            )
            self.count("can_connect", 0, tags=base_tags + ["collection:outlog"])
            raise

        pass
