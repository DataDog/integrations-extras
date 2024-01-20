from datadog_checks.base import AgentCheck
from datadog_checks.dev.utils import get_metadata_metrics

from .common import mock_http_responses


def test_check(dd_run_check, aggregator, mocked_instance, check, mocker):
    mocker.patch("requests.get", wraps=mock_http_responses)
    c = check(mocked_instance)
    dd_run_check(c)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("caddy.openmetrics.health", status=AgentCheck.OK, count=1)
