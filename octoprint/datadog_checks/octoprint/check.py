import os

import requests

from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

TIMEOUT = 10

hostname = ""
server = ""
octo_api_key = ""


class OctoPrintCheck(AgentCheck):
    def __init__(self, name, init_config, instance):
        super(OctoPrintCheck, self).__init__(name, init_config, instance)
        global hostname
        hostname = os.popen("hostname").readline().strip()
        global server
        server = "http://" + hostname
        self.log.debug('OctoPrint monitoring starting on %s', self.hostname)
        self.log.debug('octo_server: %s', server)
        global octo_api_key
        octo_api_key = self.instance.get('octo_api_key')
        self.log.debug('octo_api_key (from config): %s', octo_api_key)

    def get_rpi_core_temp(self):
        if os.path.isfile("/usr/bin/vcgencmd"):
            temp, err, retcode = get_subprocess_output(
                ["/usr/bin/vcgencmd", "measure_temp"], self.log, raise_on_empty_output=True
            )
            self.log.debug('rpi core temp - temp: %s', temp)
            self.log.debug('rpi core temp - err: %s', err)
            self.log.debug('rpi core temp - retcode: %s', retcode)
            temp = temp.replace("temp=", "").replace("'C", "")
            if temp.startswith("VCHI initialization failed"):
                self.log.info(
                    "Unable to get rPi temp.  To resolve, add the 'video' group to the 'dd-agent' user"
                    " by running `sudo usermod -aG video dd-agent`"
                )
            temp = 0.0
        elif os.path.isfile("/sys/class/thermal/thermal_zone0/temp"):
            temp, err, retcode = get_subprocess_output(
                ["cat", "/sys/class/thermal/thermal_zone0/temp"], self.log, raise_on_empty_output=True
            )
            temp = temp / 1000
        else:
            self.log.info(
                "The command typically used to get the core temperature, /usr/bin/vcgencmd,"
                "is not available on this system."
            )
            temp = 0.0
        return float(temp)

    def seconds_to_minutes(self, seconds):
        if not seconds:
            return 0
        else:
            return int(seconds / 60)

    # Get stats from REST API as json
    # def get_api_info(self, server, key, timeout, path):
    def get_api_info(self, server, key, timeout, path):
        url = server + path
        headers = {"X-Api-Key": key, "content-type": "application/json"}
        req = requests.get(url, timeout=timeout, headers=headers)
        return req.json()

    def check(self, instance):
        rpi_core_temp = self.get_rpi_core_temp()
        self.gauge("octoprint.rpi_core_temp", rpi_core_temp)

        # get job data
        job_path = "/api/job"
        job_info = self.get_api_info(server, octo_api_key, TIMEOUT, job_path)

        # # Job State
        state = job_info["state"]
        # States: Printing, Paused, Cancelled, Operational...
        if state == "Operational":
            printer_state = 0
        elif state == "Paused":
            printer_state = 1
        elif state == "Printing":
            printer_state = 2
        else:
            printer_state = -1
        self.gauge("octoprint.printer_state", printer_state)

        # Print Job Percent Completed and Time Estimate
        est_print_time = self.seconds_to_minutes(job_info["job"]["estimatedPrintTime"])
        pct_completed = job_info["progress"]["completion"]
        self.gauge("octoprint.est_print_time", est_print_time)
        self.gauge("octoprint.pct_completed", pct_completed)

        # Print Job Elapsed and Remaining Times
        print_job_time = self.seconds_to_minutes(job_info["progress"]["printTime"])
        print_job_time_left = self.seconds_to_minutes(job_info["progress"]["printTimeLeft"])
        self.gauge("octoprint.print_job_time", print_job_time)
        self.gauge("octoprint.print_job_time_left", print_job_time_left)

        # Extruder Temperatures
        extruder_temp_path = "/api/printer/tool"
        extruder_temps = self.get_api_info(server, octo_api_key, TIMEOUT, extruder_temp_path)
        for key in extruder_temps.keys():
            toolname = key
            current_tool_temp = extruder_temps[toolname]["actual"]
            target_tool_temp = extruder_temps[toolname]["target"]
            self.gauge("octoprint." + toolname + ".current_tool_temp", current_tool_temp)
            self.gauge("octoprint." + toolname + ".target_tool_temp", target_tool_temp)

        # Bed Temperatures
        bed_temp_path = "/api/printer/bed"
        bed_temp = self.get_api_info(server, octo_api_key, TIMEOUT, bed_temp_path)
        for key in bed_temp.keys():
            bedname = key
            current_bed_temp = bed_temp[bedname]["actual"]
            target_bed_temp = bed_temp[bedname]["target"]
            self.gauge("octoprint." + bedname + ".current_bed_temp", current_bed_temp)
            self.gauge("octoprint." + bedname + ".target_bed_temp", target_bed_temp)
