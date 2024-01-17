import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.hikaricp.check import HikaricpCheck

EXPECTED_MICROMETER_METRICS = {
    "hikaricp.connections",
    "hikaricp.connections.active",
    "hikaricp.connections.idle",
    "hikaricp.connections.max",
    "hikaricp.connections.pending",
    "hikaricp.connections.timeout.count",
    "hikaricp.connections.acquire.seconds.count",
    "hikaricp.connections.acquire.seconds.max",
    "hikaricp.connections.acquire.seconds.sum",
    "hikaricp.connections.creation.seconds.count",
    "hikaricp.connections.creation.seconds.sum",
    "hikaricp.connections.creation.seconds.max",
    "hikaricp.connections.usage.seconds.max",
    "hikaricp.connections.usage.seconds.count",
    "hikaricp.connections.usage.seconds.sum",
}

EXPECTED_PROMETHEUS_METRICS = {
    "hikaricp.connections",
    "hikaricp.connections.active",
    "hikaricp.connections.idle",
    "hikaricp.connections.max",
    "hikaricp.connections.min",
    "hikaricp.threads.pending",
    "hikaricp.connections.timeout.count",
    "hikaricp.connections.acquired.nanos.count",
    "hikaricp.connections.acquired.nanos.sum",
    "hikaricp.connections.acquired.nanos.quantile",
    "hikaricp.connections.creation.millis.count",
    "hikaricp.connections.creation.millis.sum",
    "hikaricp.connections.creation.millis.quantile",
    "hikaricp.connections.usage.millis.count",
    "hikaricp.connections.usage.millis.sum",
    "hikaricp.connections.usage.millis.quantile",
}


@pytest.mark.unit
def test_mock_assert_micrometer_metrics(dd_run_check, aggregator, check, mock_micrometer_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_MICROMETER_METRICS:
        aggregator.assert_metric(metric_name)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("hikaricp.openmetrics.health", status=HikaricpCheck.OK)


@pytest.mark.unit
def test_mock_assert_prometheus_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("hikaricp.openmetrics.health", status=HikaricpCheck.OK)
