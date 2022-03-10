import mock
import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.pulsar import PulsarCheck

CHECK_NAME = 'pulsar'

data = """# TYPE pulsar_consumer_available_permits untyped
pulsar_consumer_available_permits{component="broker",topic="persistent://tn/namesapce/topic"} 905 1597685608294
# TYPE pulsar_consumer_blocked_on_unacked_messages untyped
pulsar_consumer_blocked_on_unacked_messages{component="broker",topic="persistent://tn/namesapce/topic"} 0 1597685608294
# TYPE pulsar_consumer_msg_rate_out untyped
pulsar_consumer_msg_rate_out{component="broker",topic="persistent://tn/namesapce/topic"} 0.016 1597685608294
# TYPE pulsar_consumer_msg_rate_redeliver untyped
pulsar_consumer_msg_rate_redeliver{component="broker",topic="persistent://tn/namesapce/topic"} 0 1597685608294
# TYPE pulsar_consumer_msg_throughput_out gauge
pulsar_consumer_msg_throughput_out{component="broker",topic="persistent://tn/namesapce/topic"} 1.833 1597685608294
# TYPE pulsar_consumer_unacked_messages untyped
pulsar_consumer_unacked_messages{component="broker",topic="persistent://tn/namesapce/topic"} 0 1597685608294"""

data2 = """# TYPE px_cluster_cpu_percent gauge
px_cluster_cpu_percent{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 0.76 1597685608294
pulsar_consumer_rate_in{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 0.77 1597685608294
px_cluster_disk_available_bytes{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 1.3470091182e+11
px_cluster_disk_total_bytes{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 1.37438953472e+11
px_cluster_disk_utilized_bytes{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 2.738041652e+09
px_cluster_pendingio{cluster="clusterpaul",node="devbox",node_id="f5a046be5c3d"} 0"""


@pytest.mark.unit
def test_check(aggregator, mock_agent_data):
    instance = {'prometheus_url': 'http://localhost:9018/metrics'}
    check = PulsarCheck(CHECK_NAME, {}, [instance])
    check.check(instance)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    # aggregator.assert_metric("pulsar.consumer_msg_throughput_out", count=1)


def test_check_all_metrics(aggregator):
    instance = {'prometheus_url': 'http://localhost:1337/metrics'}
    check = PulsarCheck(CHECK_NAME, {}, [instance])
    response = mock.MagicMock(
        status_code=200, headers={"Content-Type": "text/plain"}, iter_lines=lambda **kw: data.split("\n")
    )
    with mock.patch("requests.get", return_value=response):
        check.check(instance)

    aggregator.assert_metric("kesque.pulsar.consumer.msg_throughput_out", count=1, value=1.833)
    # aggregator.assert_metric("pulsar.cluster.cpu_percent", count=1, value=0.76)
    # aggregator.assert_metric("pulsar.consumer.rate_in", count=1, value=0.77)
