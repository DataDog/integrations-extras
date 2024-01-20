import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.dev.utils import get_metadata_metrics

pytestmark = [pytest.mark.usefixtures("dd_environment")]


def test_check(dd_run_check, aggregator, check, instance):
    dd_run_check(check(instance))

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("caddy.openmetrics.health", status=AgentCheck.OK)
