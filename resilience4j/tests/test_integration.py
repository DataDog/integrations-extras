import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.resilience4j import Resilience4jCheck

from .common import EXPECTED_PROMETHEUS_METRICS

pytestmark = [
    pytest.mark.integration,
    pytest.mark.usefixtures("dd_environment"),
]


def test_metrics_coverage(dd_run_check, aggregator, check, mock_prometheus_metrics):
    """
    Test to ensure all expected Prometheus metrics are present.
    """
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=0)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_connect_ok(dd_run_check, aggregator, check, mock_prometheus_metrics):
    """
    Test to ensure the service check health status is appropriately set.
    """
    dd_run_check(check)

    # Assert that the service check is OK
    aggregator.assert_service_check(
        "resilience4j.openmetrics.health",
        status=Resilience4jCheck.OK,
        count=1,
    )
