import pytest

from datadog_checks.dev.utils import get_metadata_metrics

from .common import EXPECTED_METRICS


@pytest.mark.usefixtures('dd_environment')
@pytest.mark.e2e
def test_e2e(dd_agent_check, instance_e2e):
    aggregator = dd_agent_check(instance_e2e)

    for metric in EXPECTED_METRICS:
        aggregator.assert_metric(metric, at_least=0)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
