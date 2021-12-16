from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.headers import headers


class NextcloudCheck(AgentCheck):
    STATUS_CHECK = 'nextcloud.can_connect'

    METRICS_PREFIX = "nextcloud"
    METRICS_GAUGES = [
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
        "server.php.memory_limit",
        "server.php.max_execution_time",
        "server.php.upload_max_filesize",
        "server.database.size",
        "activeUsers.last5minutes",
        "activeUsers.last1hour",
        "activeUsers.last24hours",
    ]

    # Tags that will be applied to all metrics
    GLOBAL_TAGS = [
        {"name": "nextcloud_version", "json_path": "nextcloud.system.version"},
        {"name": "php_version", "json_path": "server.php.version"},
        {"name": "database_type", "json_path": "server.database.type"},
        {"name": "database_version", "json_path": "server.database.version"},
    ]

    def check(self, _):
        url = self.instance['url']

        try:
            self.log.debug("Checking against %s", url)
            response = self.http.get(url, extra_headers=headers(self.agentConfig))
            if response.status_code != 200:
                self.service_check(
                    NextcloudCheck.STATUS_CHECK, AgentCheck.CRITICAL, message="Problem requesting {}.".format(url)
                )
                return
            json_response = response.json()
            if json_response["ocs"]["meta"]["status"] == "ok":
                self.service_check(NextcloudCheck.STATUS_CHECK, AgentCheck.OK)
                self.parse_tags(json_response["ocs"]["data"])
                self.parse_metrics(json_response["ocs"]["data"])
            else:
                self.service_check(
                    NextcloudCheck.STATUS_CHECK,
                    AgentCheck.CRITICAL,
                    message="Error parsing response from {}.".format(url),
                )
        except Exception as e:
            self.service_check(
                NextcloudCheck.STATUS_CHECK, AgentCheck.CRITICAL, message="Error hitting {}. Error: {}".format(url, e)
            )

    def get_metric_display_name(self, metric_name):
        metric_display_name = metric_name
        if NextcloudCheck.METRICS_PREFIX not in metric_display_name:
            metric_display_name = "{}.{}".format(NextcloudCheck.METRICS_PREFIX, metric_name)
        return metric_display_name

    def json_nested_get(self, json_data, json_path):
        for i in json_path.split("."):
            json_data = json_data[i]
        return json_data

    def parse_tags(self, json_data):
        self.tags = list()
        for tag in NextcloudCheck.GLOBAL_TAGS:
            value = self.json_nested_get(json_data, tag["json_path"])
            self.tags.append("{}:{}".format(tag["name"], value))

    def parse_metrics(self, json_data):
        for metric in NextcloudCheck.METRICS_GAUGES:
            metric_display_name = self.get_metric_display_name(metric)
            self.gauge(metric_display_name, self.json_nested_get(json_data, metric), tags=self.tags)
