import time
from json import JSONDecodeError

# from typing import Any  # noqa: F401
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck
from datadog_checks.rundeck.config_models import ConfigMixin

from .constants import (
    DEFAULT_API_VERSION,
    EXECUTION_TAG_KEY_PREFIX,
    EXECUTIONS_RUNNING_DURATION_METRIC_NAME_PREFIX,
    EXECUTIONS_RUNNING_METRIC_NAME_PREFIX,
    METRICS_METRICS_METRIC_NAME_PREFIX,
    RUNNING_EXECUTIONS_TAG_MAP,
    SYSTEM_INFO_TAG_MAP,
    SYSTEM_METRIC_NAME_PREFIX,
    SYSTEM_METRICS_TAG_MAP,
    SYSTEM_TAG_KEY_PREFIX,
)


class RundeckCheck(ConfigMixin, AgentCheck):
    __NAMESPACE__ = "rundeck"

    def __init__(self, name, init_config, instances):
        super(RundeckCheck, self).__init__(name, init_config, instances)

        self.base_url = self.instance.get("url")
        self.api_version = self.instance.get("api_version", DEFAULT_API_VERSION)
        self.system_base_tags = []

        token = self.instance.get("access_token")
        self.http.options['headers'].update({"X-Rundeck-Auth-Token": token})

    def access_api(self, endpoint: str):
        """Call the rundeck API"""
        try:
            response = self.http.get(self.base_url + f"/api/{self.api_version}" + endpoint)
            response.raise_for_status()
            response_json = response.json()
            self.log.debug("rundeck API response(%s): %s", endpoint, response_json)
        except (HTTPError, InvalidURL, ConnectionError, Timeout):
            self.log.exception("Could not connect")
            raise
        except JSONDecodeError:
            self.log.exception("Could not parse JSON")
            raise
        except ValueError:
            self.log.exception("Unexpected value")
            raise

        return response_json

    def access_api_with_pagination(self, endpoint: str, limit: int = 20):
        """Call the rundeck API with pagination"""
        responses = []

        offset = 0
        while True:
            paginated_endpoint = f"{endpoint}?max={limit}&offset={offset}"

            response = self.access_api(paginated_endpoint)
            responses.append(response)

            paging = response.get("paging", {})
            count = paging.get("count", 0)
            offset += count

            if offset >= paging.get("total", 0):
                break

        return responses

    def check_metrics_endpoint(self):
        """Handle /metrics/metrics API"""
        metrics = self.access_api("/metrics/metrics")

        self.send_metrics_endpoint_group(metrics, "gauges", "value", self.gauge)
        self.send_metrics_endpoint_group(metrics, "counters", "count", self.monotonic_count)
        self.send_metrics_endpoint_group(metrics, "meters", "count", self.monotonic_count)

    def send_metrics_endpoint_group(self, raw_metrics, group_key, data_key, submission_method):
        """Send metrics extracted from /metrics/metrics API"""
        data = raw_metrics.get(group_key, {})
        for metric_name, metric_stats in data.items():
            metric_val = metric_stats.get(data_key)
            if metric_val is not None:
                renamed = self.rename_metric(metric_name)
                submission_method(
                    f"{METRICS_METRICS_METRIC_NAME_PREFIX}.{renamed}", metric_val, tags=self.system_base_tags
                )

    def rename_metric(self, original_name):
        """Rename the original metric name from /metrics/metrics API"""
        if original_name.startswith(f"{RundeckCheck.__NAMESPACE__}."):
            parts = original_name[8:].split(".")
        else:
            parts = original_name.split(".")

        final_parts = [self.convert_case(part) for part in parts]

        return ".".join(final_parts)

    def convert_case(self, part):
        """Convert string from camelCase or PascalCase to snake_case"""
        chars = []
        for i, char in enumerate(part):
            if char.isupper() and i > 0:
                chars.append("_")
            chars.append(char.lower())
        return "".join(chars)

    def get_nested_val(self, data, key_list):
        """Extract nested key value from a dict"""
        current_node = data
        for key in key_list:
            if isinstance(current_node, dict) and key in current_node:
                current_node = current_node[key]
            else:
                return None

        return current_node

    def check_system_info_endpoint(self):
        """Handle /system/info API"""
        system_info = self.access_api("/system/info")
        system_data = system_info.get("system")
        if system_data is None:
            self.log.error("system data not found in /system/info API response")
            return

        self.set_system_base_tags(system_data)
        self.send_system_info(system_data)

    def set_system_base_tags(self, system_data):
        """Set system base tags"""
        self.system_base_tags = [
            f"{SYSTEM_TAG_KEY_PREFIX}_{tag_key}:{tag_value}"
            for tag_key, key_list in SYSTEM_INFO_TAG_MAP.items()
            if (tag_value := self.get_nested_val(system_data, key_list)) is not None
        ]

    def send_system_info(self, system_data):
        """Send metrics extracted from /system/info API"""
        stats = system_data.get("stats")
        if stats is None:
            self.log.error("stats data not found in system data: %s", system_data)
            return

        for name, key_list in SYSTEM_METRICS_TAG_MAP.items():
            value = self.get_nested_val(stats, key_list)
            if value is not None:
                self.gauge(f"{SYSTEM_METRIC_NAME_PREFIX}.{name}", value, self.system_base_tags)

    def check_project_executions_running(self):
        """Handle /project/*/executions/running API"""
        running_executions_info = [
            execution
            for response in self.access_api_with_pagination("/project/*/executions/running")
            for execution in response["executions"]
        ]
        for execution in running_executions_info:
            self.send_running_execution(execution)

    def send_running_execution(self, execution):
        """Send metrics extracted from /project/*/executions/running API"""
        tag_list = [
            f"{EXECUTION_TAG_KEY_PREFIX}_{tag_key}:{tag_value}"
            for tag_key, key_list in RUNNING_EXECUTIONS_TAG_MAP.items()
            if (tag_value := self.get_nested_val(execution, key_list)) is not None
        ]
        tag_list.extend(self.system_base_tags)

        self.gauge(EXECUTIONS_RUNNING_METRIC_NAME_PREFIX, 1, tags=tag_list)

        started_ms = self.get_nested_val(execution, ["date-started", "unixtime"])
        if started_ms is not None:
            duration_ms = int(time.time() * 1000) - started_ms
            self.gauge(EXECUTIONS_RUNNING_DURATION_METRIC_NAME_PREFIX, duration_ms, tags=tag_list)

    def check(self, _):
        self.check_system_info_endpoint()
        self.check_metrics_endpoint()
        self.check_project_executions_running()
