import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.jfrog_platform import JfrogPlatformCheck

CHECK_NAME = 'jfrog_platform'
MOCK_ART_INSTANCE = {
    'prometheus_url': 'http://localhost:80/api/v1/metrics',
    'instance_type': 'artifactory',
}
MOCK_XRAY_INSTANCE = {
    'prometheus_url': 'http://localhost:9018/xray/api/v1/metrics',
    'instance_type': 'xray',
}


@pytest.mark.unit
def test_config():
    with pytest.raises(CheckException):
        JfrogPlatformCheck(CHECK_NAME, {}, [{}])

    JfrogPlatformCheck(CHECK_NAME, {}, [MOCK_ART_INSTANCE])


@pytest.mark.unit
def test_openmetrics_art_check(aggregator, mock_art_agent_data):
    c = JfrogPlatformCheck(CHECK_NAME, {}, [MOCK_ART_INSTANCE])
    c.check(MOCK_ART_INSTANCE)

    aggregator.assert_metric("jfrog.artifactory.jfrt_runtime_heap_processors_total", count=1, value=6)
    aggregator.assert_metric("jfrog.artifactory.jfrt_db_connections_active_total", count=1, value=2)


@pytest.mark.unit
def test_openmetrics_xray_check(aggregator, mock_xray_agent_data):
    c = JfrogPlatformCheck(CHECK_NAME, {}, [MOCK_XRAY_INSTANCE])
    c.check(MOCK_XRAY_INSTANCE)

    aggregator.assert_metric("jfrog.xray.sys_memory_free_bytes", count=1, value=5.503541248e10)
    aggregator.assert_metric("jfrog.xray.sys_memory_used_bytes", count=1, value=4.3053436928e10)
    aggregator.assert_metric("jfrog.xray.app_disk_free_bytes", count=1, value=2.079695966208e12)
    aggregator.assert_metric("jfrog.xray.app_disk_used_bytes", count=1, value=6.77750784e10)
    aggregator.assert_metric("jfrog.xray.sys_cpu_ratio", count=1, value=0.025974025534204213)

    aggregator.assert_metric(name='jfrog.xray.jfxr_data_artifacts_total', count=1, value=43.0, tags=['package_type:go'])
    aggregator.assert_metric(
        name='jfrog.xray.jfxr_data_artifacts_total', count=1, value=442.0, tags=['package_type:docker']
    )
    aggregator.assert_metric(
        name='jfrog.xray.jfxr_data_components_total', count=1, value=1892.0, tags=['package_type:maven']
    )
    aggregator.assert_metric(
        name='jfrog.xray.jfxr_data_components_total', count=1, value=11.0, tags=['package_type:rubygems']
    )

    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
def test_openmetrics_error(aggregator, instance, error_metrics):
    check = JfrogPlatformCheck(CHECK_NAME, {}, [MOCK_XRAY_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_XRAY_INSTANCE)
        aggregator.assert_metric("jfrog.artifactory.db_connections_active", count=1, value=2)
