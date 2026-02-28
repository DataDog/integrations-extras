import time
from json import JSONDecodeError

# from typing import Any  # noqa: F401
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.persistent_cache import config_set_persistent_cache_id
from datadog_checks.rundeck.config_models import ConfigMixin
from datadog_checks.rundeck.config_models.defaults import instance_api_version
from datadog_checks.rundeck.utils import get_nested_val, rename_metric

from .constants import (
    CACHE_KEY_TIMESTAMP,
    COMPLETED_EXEC_TAG_MAP,
    EXEC_COMPLETED_DURATION_METRIC_NAME,
    EXEC_RUNNING_DURATION_METRIC_NAME,
    EXEC_STATUS_METRIC_NAME,
    EXEC_STATUS_RUNNING,
    EXEC_TAG_MAP,
    EXEC_TAG_TEMPLATE,
    EXEC_TAGS_LIST_VALUED,
    METRICS_METRICS_METRIC_NAME_PREFIX,
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
        self.api_version = self.instance.get("api_version", instance_api_version())
        self.system_base_tags = []
        self.projects = []

        token = self.instance.get("access_token")
        self.http.options['headers'].update({"X-Rundeck-Auth-Token": token, "Accept": "application/json"})

    def persistent_cache_id(self):
        return config_set_persistent_cache_id(self, instance_config_options=['url', 'api_version'])

    def access_api(self, endpoint, query_params=None):
        """Call the rundeck API"""
        try:
            response = self.http.get(self.base_url + f"/api/{self.api_version}" + endpoint, params=query_params)
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

    def access_api_with_pagination(self, endpoint, limit=20, query_params=None):
        """Call the rundeck API with pagination"""
        responses = []
        offset_key = "offset"
        if query_params is None:
            query_params = {"max": limit, offset_key: 0}
        else:
            query_params["max"] = limit
            query_params[offset_key] = 0

        while True:
            response = self.access_api(endpoint, query_params)
            responses.append(response)

            paging = response.get("paging", {})
            count = paging.get("count", 0)
            query_params[offset_key] += count

            if count == 0 or query_params.get(offset_key) >= paging.get("total", 0):
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
                renamed = rename_metric(metric_name, self.__NAMESPACE__)
                submission_method(
                    f"{METRICS_METRICS_METRIC_NAME_PREFIX}.{renamed}", metric_val, tags=self.system_base_tags
                )

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
            if (tag_value := get_nested_val(system_data, key_list)) is not None
        ]

    def send_system_info(self, system_data):
        """Send metrics extracted from /system/info API"""
        stats = system_data.get("stats")
        if stats is None:
            self.log.error("stats data not found in system data: %s", system_data)
            return

        for name, key_list in SYSTEM_METRICS_TAG_MAP.items():
            value = get_nested_val(stats, key_list)
            if value is not None:
                self.gauge(f"{SYSTEM_METRIC_NAME_PREFIX}.{name}", value, self.system_base_tags)

    def check_project_executions_running(self, project_name: str):
        """Handle /project/[PROJECT]/executions/running API"""
        running_executions_info = [
            execution
            for response in self.access_api_with_pagination(f"/project/{project_name}/executions/running")
            for execution in response["executions"]
        ]
        for execution in running_executions_info:
            self.send_execution_status(execution)

    def get_completed_execution_tags(self, execution):
        """Create the list of tags for completed execution"""
        tag_list = []
        for tag_key, key_list in COMPLETED_EXEC_TAG_MAP.items():
            tag_value = get_nested_val(execution, key_list)
            if tag_value is None:
                continue

            values = tag_value if tag_key in EXEC_TAGS_LIST_VALUED else [tag_value]
            for value in values:
                tag_list.append(EXEC_TAG_TEMPLATE.format(key=tag_key, value=value))
        return tag_list

    def send_execution_status(self, execution):
        """Send status & duration metrics extracted from execution"""
        tag_list = [
            EXEC_TAG_TEMPLATE.format(key=tag_key, value=tag_value)
            for tag_key, key_list in EXEC_TAG_MAP.items()
            if (tag_value := get_nested_val(execution, key_list)) not in (None, "")
        ]
        if execution.get("status") != EXEC_STATUS_RUNNING:
            completed_tag_list = self.get_completed_execution_tags(execution)
            tag_list.extend(completed_tag_list)
        tag_list.extend(self.system_base_tags)

        self.gauge(EXEC_STATUS_METRIC_NAME, 1, tags=tag_list)
        self.send_execution_duration(execution, tag_list)
        self.log.info("rundeck sent %s metric. %s", execution["status"], execution)

    def send_execution_duration(self, execution, execution_tags):
        """Send duration metrics for each execution"""
        started_ms = get_nested_val(execution, ["date-started", "unixtime"])
        if started_ms is None:
            self.log.warning("Unable to send duration metric. started-ms missing from execution.")
            return

        if execution.get("status") == EXEC_STATUS_RUNNING:
            duration_ms = int(time.time() * 1000) - started_ms
            self.gauge(EXEC_RUNNING_DURATION_METRIC_NAME, duration_ms, tags=execution_tags)
            return

        # execution completed
        ended_ms = get_nested_val(execution, ["date-ended", "unixtime"])
        if ended_ms is None:
            self.log.warning("Unable to send duration metric. ended-ms missing from execution.")
            return
        duration_ms = ended_ms - started_ms
        self.gauge(EXEC_COMPLETED_DURATION_METRIC_NAME, duration_ms, tags=execution_tags)

    def check_project_executions_completed(self, begin: int, end: int, project_name: str):
        """Handle /project/[PROJECT]/executions API"""
        param = {"begin": begin, "end": end}

        completed_executions_info = [
            execution
            for response in self.access_api_with_pagination(f"/project/{project_name}/executions", query_params=param)
            for execution in response["executions"]
        ]
        for execution in completed_executions_info:
            self.send_execution_status(execution)

    def check_project_executions(self, begin: int | None, end: int):
        """Check all projects executions"""
        for project in self.projects:
            name = project.get("name")
            if name is None:
                self.log.warning("Unable to send metrics for project. Name missing from project.")
                continue

            self.check_project_executions_running(name)
            if begin is not None:
                self.check_project_executions_completed(begin, end, name)

    def check_project_endpoint(self):
        """Handle /projects API"""
        self.projects = self.access_api("/projects")

    def check(self, _):
        last_timestamp = (
            None if (cache_value := self.read_persistent_cache(CACHE_KEY_TIMESTAMP)) == "" else int(cache_value)
        )
        now_timestamp = time.time_ns() // 1_000_000

        self.check_project_endpoint()
        self.check_system_info_endpoint()
        self.check_metrics_endpoint()
        self.check_project_executions(last_timestamp, now_timestamp)

        self.write_persistent_cache(CACHE_KEY_TIMESTAMP, str(now_timestamp))
