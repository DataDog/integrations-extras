import pytest
import HikaricpCheck

from datadog_checks.dev.utils import get_metadata_metrics

EXPECTED_METRICS = {
    "hikaricp.connections",
    "hikaricp.connections.active",
    "hikaricp.connections.idle",
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


@pytest.mark.unit
def test_mock_assert_metrics(dd_run_check, aggregator, check, mock_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_METRICS:
        aggregator.assert_metric(metric_name)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("hikaricp.openmetrics.health", status=HikaricpCheck.OK)    
