import pytest

from datadog_checks.cyral.cyral import CyralCheck

CHECK_NAME = 'cyral'


@pytest.mark.unit
def test_check_all_metrics(aggregator, mock_agent_data):
    instance = {'prometheus_url': 'http://localhost:9018/metrics'}
    c = CyralCheck(CHECK_NAME, {}, [instance])
    c.check(instance)
    aggregator.assert_metric("cyral.analysis_time", count=1, value=2.274237)
