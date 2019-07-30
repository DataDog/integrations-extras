import pytest
import mock

from datadog_checks.checks import AgentCheck
from datadog_checks.ping import PingCheck
from datadog_checks.errors import CheckException


def mock_exec_ping():
    return """FAKEPING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.093 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 0.093/0.093/0.093/0.000 ms"""


def test_empty_check(empty_instance):
    check = PingCheck('ping', {}, {})

    # empty instance
    with pytest.raises(CheckException):
        check.check(empty_instance)


def test_incorrect_ip_check(incorrect_ip_instance):
    check = PingCheck('ping', {}, {})

    # empty instance
    with pytest.raises(CheckException):
        check.check(incorrect_ip_instance)


def test_valid_check(aggregator, instance):
    check = PingCheck('ping', {}, {})

    with mock.patch.object(check, "_exec_ping", return_value=mock_exec_ping()):
        check.check(instance)
    aggregator.assert_service_check('network.ping.can_connect', AgentCheck.OK)
    aggregator.assert_metric('network.ping.can_connect', value=1)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("dd_environment")
def test_integration(aggregator, instance):
    check = PingCheck('ping', {}, {})
    check.check(instance)

    tags = ["ping1", "ping2", "target_host:127.0.0.1"]

    aggregator.assert_service_check('network.ping.can_connect', AgentCheck.OK)
    aggregator.assert_metric('network.ping.can_connect', value=1, tags=tags)
    aggregator.assert_all_metrics_covered()
