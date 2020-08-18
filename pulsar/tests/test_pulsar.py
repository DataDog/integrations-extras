import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.pulsar import PulsarCheck

CHECK_NAME = 'pulsar'


@pytest.mark.unit
def test_check(aggregator, mock_agent_data):
    instance = {'prometheus_url': 'http://localhost:9018/metrics'}
    check = PulsarCheck(CHECK_NAME, {}, [instance])
    check.check(instance)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
