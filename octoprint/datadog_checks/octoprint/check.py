import os
from copy import copy

import requests

from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

TIMEOUT = 10
JOB_URL = "/api/job"
EXTRUDER_URL = "/api/printer/tool"
BED_URL = "/api/printer/bed"


class OctoPrintCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(OctoPrintCheck, self).__init__(name, init_config, instances)

        self.url = self.instance.get('url')
        self.octo_api_key = self.instance.get('octo_api_key')
        self.tags = self.instance.get('tags', [])

        self.log.debug('OctoPrint monitoring starting on %s', self.url)

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
    def get_api_info(self, path):
        url = self.url + path
        key = self.octo_api_key
        headers = {"X-Api-Key": key, "content-type": "application/json"}
        req = requests.get(url, timeout=TIMEOUT, headers=headers)
        return req.json()

    def check(self, instance):
        tags = copy(self.tags)

        rpi_core_temp = self.get_rpi_core_temp()
        self.gauge("octoprint.rpi_core_temp", rpi_core_temp, tags=tags)

        # get job data
        job_info = self.get_api_info(JOB_URL)

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
        self.gauge("octoprint.printer_state", printer_state, tags=tags)

        # Print Job Percent Completed and Time Estimate if Job Active
        est_print_time = self.seconds_to_minutes(job_info["job"]["estimatedPrintTime"])
        if est_print_time > 0:
            pct_completed = job_info["progress"]["completion"]
            print('type of est print time: {}'.format(type(est_print_time)))
            self.gauge("octoprint.est_print_time", est_print_time, tags=tags)
            self.gauge("octoprint.pct_completed", pct_completed, tags=tags)

            # Print Job Elapsed and Remaining Times
            print_job_time = self.seconds_to_minutes(job_info["progress"]["printTime"])
            print_job_time_left = self.seconds_to_minutes(job_info["progress"]["printTimeLeft"])
            self.gauge("octoprint.print_job_time", print_job_time, tags=tags)
            self.gauge("octoprint.print_job_time_left", print_job_time_left, tags=tags)

        # Extruder Temperatures
        extruder_temps = self.get_api_info(EXTRUDER_URL)
        for key in extruder_temps.keys():
            tooltags = tags + ['toolname:' + key]
            current_tool_temp = extruder_temps[key]["actual"]
            target_tool_temp = extruder_temps[key]["target"]
            self.gauge("octoprint.current_tool_temp", current_tool_temp, tags=tooltags)
            self.gauge("octoprint.target_tool_temp", target_tool_temp, tags=tooltags)

        # Bed Temperatures
        bed_temp = self.get_api_info(BED_URL)
        for key in bed_temp.keys():
            bedtags = tags + ['bedname:' + key]
            current_bed_temp = bed_temp[key]["actual"]
            target_bed_temp = bed_temp[key]["target"]
            self.gauge("octoprint.current_bed_temp", current_bed_temp, tags=bedtags)
            self.gauge("octoprint.target_bed_temp", target_bed_temp, tags=bedtags)
