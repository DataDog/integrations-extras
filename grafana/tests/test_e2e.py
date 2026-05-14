import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics


@pytest.mark.e2e
def test_metrics(dd_agent_check):
    aggregator = dd_agent_check(check_rate=True)

    aggregator.assert_metric("grafana.build_info")
    aggregator.assert_service_check('grafana.openmetrics.health', ServiceCheck.OK, at_least=1)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
