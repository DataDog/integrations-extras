import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.jfrog_metrics import JfrogMetricsCheck

CHECK_NAME = 'jfrog_metrics'
MOCK_ART_INSTANCE = {
    'prometheus_url': 'http://localhost:80/api/v1/metrics',
}
MOCK_XRAY_INSTANCE = {
    'prometheus_url': 'http://localhost:9018/xray/api/v1/metrics',
}


@pytest.mark.unit
def test_config():
    with pytest.raises(CheckException):
        JfrogMetricsCheck(CHECK_NAME, {}, 'art', [{}])

    JfrogMetricsCheck(CHECK_NAME, {}, 'art', [MOCK_ART_INSTANCE])


@pytest.mark.unit
def test_openmetrics_art_check(aggregator, mock_art_agent_data):
    c = JfrogMetricsCheck(CHECK_NAME, {}, 'art', [MOCK_ART_INSTANCE])
    c.check(MOCK_ART_INSTANCE)

    aggregator.assert_metric("jfrog.artifactory.runtime_heap_processors", count=1, value=6)
    aggregator.assert_metric("jfrog.artifactory.db_connections_active", count=1, value=2)


@pytest.mark.unit
def test_openmetrics_xray_check(aggregator, mock_xray_agent_data):
    c = JfrogMetricsCheck(CHECK_NAME, {}, 'xray', [MOCK_XRAY_INSTANCE])
    c.check(MOCK_XRAY_INSTANCE)

    aggregator.assert_metric("jfrog.xray.sys_memory_used", count=1, value=20)


@pytest.mark.unit
def test_openmetrics_error(aggregator, instance, error_metrics):
    check = JfrogMetricsCheck(CHECK_NAME, {}, 'xray', [MOCK_XRAY_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_XRAY_INSTANCE)
        aggregator.assert_metric("jfrog.artifactory.db_connections_active", count=1, value=2)
