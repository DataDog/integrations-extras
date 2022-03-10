import mock

from datadog_checks.portworx.portworx import PortworxCheck

CHECK_NAME = 'portworx'


data = """# TYPE px_cluster_cpu_percent gauge
px_cluster_cpu_percent{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 0.76
px_cluster_disk_available_bytes{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 1.3470091182e+11
px_cluster_disk_total_bytes{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 1.37438953472e+11
px_cluster_disk_utilized_bytes{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 2.738041652e+09
px_cluster_memory_utilized_percent{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 24
px_cluster_pendingio{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 0"""


def test_check_all_metrics(aggregator):
    instance = {'prometheus_endpoint': 'http://localhost:1337/metrics'}
    check = PortworxCheck(CHECK_NAME, {}, {})
    response = mock.MagicMock(
        status_code=200, headers={"Content-Type": "text/plain"}, iter_lines=lambda **kw: data.split("\n")
    )
    with mock.patch("requests.get", return_value=response):
        check.check(instance)

    aggregator.assert_metric("portworx.cluster.cpu_percent", count=1, value=0.76)
