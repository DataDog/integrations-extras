from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.headers import headers

import requests


STATUS_CHECK = 'nextcloud.can_connect'

NEXTCLOUD_METRICS_PREFIX = "nextcloud"
NEXTCLOUD_METRICS_GAUGES = [
    "nextcloud.system.freespace",
    "nextcloud.system.apps.num_installed",
    "nextcloud.system.apps.num_updates_available",
    "nextcloud.storage.num_users",
    "nextcloud.storage.num_files",
    "nextcloud.storage.num_storages",
    "nextcloud.storage.num_storages_local",
    "nextcloud.storage.num_storages_home",
    "nextcloud.storage.num_storages_other",
    "nextcloud.shares.num_shares",
    "nextcloud.shares.num_shares_user",
    "nextcloud.shares.num_shares_groups",
    "nextcloud.shares.num_shares_link_no_password",
    "nextcloud.shares.num_fed_shares_sent",
    "nextcloud.shares.num_fed_shares_received",
    "server.database.size",
    "activeUsers.last5minutes",
    "activeUsers.last1hour",
    "activeUsers.last24hours"
]


class NextcloudCheck(AgentCheck):
    def check(self, instance):
        url = instance['url']
        username = instance['username']
        password = instance['password']
        auth = (username, password)

        try:
            self.log.debug("Checking against {}".format(url))
            response = requests.get(
                url, auth=auth, headers=headers(self.agentConfig)
            )
            if response.status_code != 200:
                self.service_check(
                    STATUS_CHECK,
                    AgentCheck.CRITICAL,
                    message="Problem requesting {}.".format(url),
                )
                return
            json_response = response.json()
            if json_response["ocs"]["meta"]["status"] == "ok":
                self.service_check(STATUS_CHECK, AgentCheck.OK)
                self.parse_metrics(json_response["ocs"]["data"])
            else:
                self.service_check(
                    STATUS_CHECK,
                    AgentCheck.CRITICAL,
                    message="Error parsing response from {}.".format(url),
                )
        except Exception as e:
            self.service_check(
                STATUS_CHECK,
                AgentCheck.CRITICAL,
                message="Error hitting {}. Error: {}".format(url, e),
            )

    def json_nested_get(self, json_data, metric_path):
        for i in metric_path.split("."):
            json_data = json_data[i]
        return json_data

    def parse_metrics(self, json_data):
        for metric in NEXTCLOUD_METRICS_GAUGES:
            metric_display_name = metric
            if NEXTCLOUD_METRICS_PREFIX not in metric_display_name:
                metric_display_name = "{}.{}".format(NEXTCLOUD_METRICS_PREFIX, metric)

            self.gauge(metric_display_name, self.json_nested_get(json_data, metric))
