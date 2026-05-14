import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.resilience4j import Resilience4jCheck

from .common import EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.usefixtures("dd_environment"), pytest.mark.e2e]


def test_e2e_resilience4j_service_check_ok(dd_run_check, aggregator, check, mock_prometheus_metrics):
    """Test that service check is OK when the endpoint is accessible and returns valid metrics."""
    dd_run_check(check)

    # Assert that the health service check is OK
    aggregator.assert_service_check('resilience4j.openmetrics.health', ServiceCheck.OK)


def test_e2e_resilience4j_service_check_critical_on_connection_error(dd_run_check, aggregator):
    # Create instance with invalid endpoint to force connection error
    bad_check = Resilience4jCheck(
        'resilience4j', {}, [{'prometheus_url': 'http://invalid-host:9999/actuator/prometheus'}]
    )

    # Run check - should fail with connection error and raise exception
    # OpenMetrics-based checks don't send service checks when connection fails, they just raise
    with pytest.raises(Exception):
        dd_run_check(bad_check)

    # No service checks should be sent when connection fails
    all_service_checks = aggregator._service_checks
    assert len(all_service_checks) == 0, f"Expected no service checks, but got: {all_service_checks}"


def test_e2e_resilience4j_check_e2e_assert_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=0)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
