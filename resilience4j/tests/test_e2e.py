import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.resilience4j import Resilience4jCheck

from .common import EXPECTED_PROMETHEUS_METRICS, INSTANCE

pytestmark = [pytest.mark.e2e]


def test_resilience4j_e2e(dd_run_check, aggregator, check):
    check = Resilience4jCheck("resilience4j", {}, [INSTANCE])
    dd_run_check(check)

    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=0)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check(
        "resilience4j.openmetrics.health",
        status=Resilience4jCheck.OK,
        count=1,
    )
