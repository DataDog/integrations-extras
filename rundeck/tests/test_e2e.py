import time
import pytest
import requests

from datadog_checks.dev import get_docker_hostname
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.rundeck.constants import (
    EXEC_COMPLETED_DURATION_METRIC_NAME,
    EXEC_RUNNING_DURATION_METRIC_NAME,
    EXEC_STATUS_METRIC_NAME,
    EXEC_TAG_KEY_PREFIX,
    METRICS_METRICS_METRIC_NAME_PREFIX,
    SYSTEM_METRIC_NAME_PREFIX,
    SYSTEM_METRICS_TAG_MAP,
    SYSTEM_TAG_KEY_PREFIX,
)


@pytest.mark.e2e
def test_e2e_rundeck(dd_agent_check, instance):
    dd_agent_check(instance)
    # trigger fast job to ensure metric produced
    for job in ["1fastjob-pass-1111-1111-111111111111", "1fastjob-fail-1111-1111-111111111111"]:
        requests.post(
            f"http://{get_docker_hostname()}:4440/api/30/job/{job}/run",
            headers={"X-Rundeck-Auth-Token": "my-static-token-123"},
        )
    time.sleep(3)
    aggregator = dd_agent_check(instance, rate=2)

    # check /system/info metrics
    for name_postfix in SYSTEM_METRICS_TAG_MAP:
        expected_name = f"rundeck.{SYSTEM_METRIC_NAME_PREFIX}.{name_postfix}"
        aggregator.assert_metric(expected_name, metric_type=0)
        aggregator.assert_metric_has_tag_prefix(expected_name, SYSTEM_TAG_KEY_PREFIX)

    # check /metrics/metrics metrics
    candidates = [
        name for name in aggregator.metric_names if name.startswith(f"rundeck.{METRICS_METRICS_METRIC_NAME_PREFIX}")
    ]
    for name in candidates:
        aggregator.assert_metric_has_tag_prefix(name, SYSTEM_TAG_KEY_PREFIX)

    # check execution status metric
    status_metric_name = f"rundeck.{EXEC_STATUS_METRIC_NAME}"
    aggregator.assert_metric(status_metric_name, value=1)
    aggregator.assert_metric_has_tag_prefix(status_metric_name, SYSTEM_TAG_KEY_PREFIX)
    aggregator.assert_metric_has_tag_prefix(status_metric_name, EXEC_TAG_KEY_PREFIX)

    # check execution duration metric
    for name_postfix in [EXEC_RUNNING_DURATION_METRIC_NAME, EXEC_COMPLETED_DURATION_METRIC_NAME]:
        metric_name = f"rundeck.{name_postfix}"
        aggregator.assert_metric_has_tag_prefix(metric_name, SYSTEM_TAG_KEY_PREFIX)
        aggregator.assert_metric_has_tag_prefix(metric_name, EXEC_TAG_KEY_PREFIX)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
