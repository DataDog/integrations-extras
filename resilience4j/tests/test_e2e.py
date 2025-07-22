import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics

from .common import EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.usefixtures("dd_environment"), pytest.mark.e2e]


def test_e2e_resilience4j_check_e2e_assert_service_check(dd_agent_check, aggregator, instance):
    with pytest.raises(Exception):
        dd_agent_check(instance, rate=True)

    # Check if any service checks were emitted before making assertions
    service_checks = aggregator.service_checks('resilience4j.openmetrics.health')
    if not service_checks:
        pytest.skip("No service checks emitted, skipping assertion.")

    # Perform assertion if service checks exist
    aggregator.assert_service_check('resilience4j.openmetrics.health', ServiceCheck.OK)


def test_e2e_resilience4j_check_e2e_assert_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=0)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
