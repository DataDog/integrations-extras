import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.rundeck.constants import (
    EXECUTION_TAG_KEY_PREFIX,
    EXECUTIONS_RUNNING_DURATION_METRIC_NAME_PREFIX,
    EXECUTIONS_RUNNING_METRIC_NAME_PREFIX,
    METRICS_METRICS_METRIC_NAME_PREFIX,
    SYSTEM_METRIC_NAME_PREFIX,
    SYSTEM_METRICS_TAG_MAP,
    SYSTEM_TAG_KEY_PREFIX,
)

@pytest.mark.e2e
def test_e2e_rundeck(dd_agent_check, instance):
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

    # check /project/*/executions/running metrics
    for name_postfix in [EXECUTIONS_RUNNING_METRIC_NAME_PREFIX, EXECUTIONS_RUNNING_DURATION_METRIC_NAME_PREFIX]:
        expected_name = f"rundeck.{name_postfix}"
        aggregator.assert_metric(expected_name, metric_type=0)
        aggregator.assert_metric_has_tag_prefix(expected_name, EXECUTION_TAG_KEY_PREFIX)

    aggregator.assert_all_metrics_covered()

    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
