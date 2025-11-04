from pathlib import Path

import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.grafana import GrafanaCheck

from .common import METRICS


def test_check(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(file_path=Path(__file__).parent.absolute() / "fixtures" / "grafana_metrics.txt")
    check = GrafanaCheck('grafana', {}, [instance])
    dd_run_check(check)
    for m in METRICS:
        aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(status_code=404)
    check = GrafanaCheck('grafana', {}, [instance])
    with pytest.raises(Exception, match="requests.exceptions.HTTPError"):
        dd_run_check(check)
    aggregator.assert_service_check('grafana.openmetrics.health', GrafanaCheck.CRITICAL)
