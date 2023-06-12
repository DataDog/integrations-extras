
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
# from datadog_checks.base import OpenMetricsBaseCheckV2

class WayfinderCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'wayfinder'

    def __init__(self, name, init_config, instances):
        super(WayfinderCheck, self).__init__(name, init_config, instances)

        # Use self.instance to read the check configuration
        self.terranetes_controller_url = self.instance.get("terranetes_controller_url")

    def _http_check(self, url, check_name):
        try:
            response = self.http.get(url)
            response.raise_for_status()
        except Exception as e:
            self.service_check(check_name, self.CRITICAL, message=str(e))
        else:
            if response.status_code == 200:
                self.service_check(check_name, self.OK)
            else:
                self.service_check(check_name, self.WARNING)

    def check(self, _):
        # Terranetes health endpoint
        terranetes_health_url = self.terranetes_controller_url + "/healthz"
        self._http_check(terranetes_health_url, 'terranetes_controller.health')
