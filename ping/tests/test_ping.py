import mock
import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException
from datadog_checks.ping import PingCheck


def mock_exec_ping():
    return """FAKEPING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.093 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 0.093/0.093/0.093/0.000 ms"""


def mock_exec_ping_german():
    return (
        "Antwort von 127.0.0.1: Bytes=32 Zeit=3ms TTL=117\n"
        "Ping-Statistik für 127.0.0.1:\n"
        "    Minimum = 3ms, Maximum = 3ms, Mittelwert = 3ms"
    )


def test_empty_check(empty_instance):
    check = PingCheck("ping", {}, {})

    with pytest.raises(CheckException):
        check.check(empty_instance)


def test_incorrect_ip_check(incorrect_ip_instance):
    check = PingCheck("ping", {}, {})

    with pytest.raises(CheckException):
        check.check(incorrect_ip_instance)


def test_valid_check(aggregator, instance):
    check = PingCheck("ping", {}, {})

    with mock.patch.object(check, "_exec_ping", return_value=mock_exec_ping()):
        check.check(instance)
    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.OK)
    aggregator.assert_metric("network.ping.can_connect", value=1)
    aggregator.assert_all_metrics_covered()


def test_valid_check_ipv6(aggregator, instance_ipv6):
    check = PingCheck("ping", {}, {})

    with mock.patch.object(check, "_exec_ping", return_value=mock_exec_ping()):
        check.check(instance_ipv6)
    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.OK)
    aggregator.assert_metric("network.ping.can_connect", value=1)
    aggregator.assert_all_metrics_covered()


def test_localized_output(aggregator, instance_response_time):
    check = PingCheck("ping", {}, {})

    with mock.patch.object(check, "_exec_ping", return_value=mock_exec_ping_german()):
        check.check(instance_response_time)
    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.OK)
    aggregator.assert_metric("network.ping.can_connect", value=1)
    aggregator.assert_metric("network.ping.response_time", value=3)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("dd_environment")
def test_integration(aggregator, instance):
    check = PingCheck("ping", {}, {})
    check.check(instance)

    tags = ["ping1", "ping2"]
    all_tags = tags.append("target_host:127.0.0.1")

    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.OK)
    aggregator.assert_metric("network.ping.can_connect", value=1, tags=all_tags)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("dd_environment")
def test_integration_ipv6(aggregator, instance_ipv6):
    check = PingCheck("ping", {}, {})
    check.check(instance_ipv6)

    tags = ["ping1", "ping2"]
    all_tags = tags.append("target_host:0000:0000:0000:0000:0000:0000:0000:0001")

    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.OK)
    aggregator.assert_metric("network.ping.can_connect", value=1, tags=all_tags)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("dd_environment")
def test_integration_response_time(aggregator, instance_response_time):
    check = PingCheck("ping", {}, {})
    check.check(instance_response_time)

    tags = ["response_time:yes"]
    all_tags = tags.append("target_host:127.0.0.1")

    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.OK)
    aggregator.assert_metric("network.ping.can_connect", value=1, tags=all_tags)
    aggregator.assert_metric("network.ping.response_time", tags=all_tags)
    aggregator.assert_all_metrics_covered()
