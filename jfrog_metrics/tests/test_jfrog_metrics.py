import pytest

from datadog_checks.jfrog_metrics import JfrogMetricsCheck

CHECK_NAME = 'jfrog_metrics'


@pytest.mark.unit
def test_check_all_metrics(aggregator, mock_agent_data):
    instance = {'prometheus_url': 'http://localhost:9018/metrics'}
    c = JfrogMetricsCheck(CHECK_NAME, {}, [instance])
    c.check(instance)
    aggregator.assert_metric("jfrog_artifactory.jfrt_runtime_heap_processors_total", count=1, value=6)
    aggregator.assert_metric("jfrog_artifactory.jfrt_db_connections_active_total", count=1, value=2)
