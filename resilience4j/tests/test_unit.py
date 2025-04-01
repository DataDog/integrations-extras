import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.resilience4j import Resilience4jCheck

from .common import BAD_HOSTNAME_INSTANCE, EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.unit]


def test_connect_exception(dd_run_check, aggregator, caplog):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = Resilience4jCheck("resilience4j", {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check("resilience4j.openmetrics.health", status=Resilience4jCheck.CRITICAL)


def test_common_resilience4j_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=0)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
