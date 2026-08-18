import platform
import subprocess

import mock
import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException
from datadog_checks.ping import PingCheck

WINDOWS_GERMAN_OUTPUT = (
    "Ping wird ausgeführt für 127.0.0.1 mit 32 Bytes Daten:\r\nAntwort von 127.0.0.1: Bytes=32 Zeit=3ms TTL=117\r\n"
).encode("cp850")


def run_windows_check(check, instance, stdout=b"", stderr=b"", returncode=0, run_side_effect=None):
    check.WINDOWS_OUTPUT_ENCODING = "cp850"
    proc = mock.Mock(stdout=stdout, stderr=stderr, returncode=returncode)
    run_mock = mock.Mock(return_value=proc, side_effect=run_side_effect)
    with mock.patch.object(platform, "system", return_value="Windows"), mock.patch.object(subprocess, "run", run_mock):
        check.check(instance)


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


def test_windows_oem_decode():
    check = PingCheck("ping", {}, {})
    check.WINDOWS_OUTPUT_ENCODING = "cp850"
    proc = mock.Mock(stdout=WINDOWS_GERMAN_OUTPUT, stderr=b"", returncode=0)
    with mock.patch.object(subprocess, "run", return_value=proc):
        lines, err, retcode = check._exec_ping_windows(["ping", "-n", "1", "127.0.0.1"], 14)
    # The actual regression check: a wrong codec turns "ausgeführt" into mojibake / replacement chars.
    assert "ausgeführt" in lines
    assert "\ufffd" not in lines


def test_windows_missing_executable_is_critical(aggregator, instance):
    check = PingCheck("ping", {}, {})
    with pytest.raises(CheckException):
        run_windows_check(check, instance, run_side_effect=FileNotFoundError("ping6"))
    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.CRITICAL)


def test_windows_nonzero_return_code_is_critical(aggregator, instance):
    check = PingCheck("ping", {}, {})
    with pytest.raises(CheckException):
        run_windows_check(check, instance, stdout=b"Request timed out.\r\n", returncode=1)
    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.CRITICAL)


def test_windows_empty_output_is_critical(aggregator, instance):
    check = PingCheck("ping", {}, {})
    with pytest.raises(CheckException):
        run_windows_check(check, instance, stdout=b"")
    aggregator.assert_service_check("network.ping.can_connect", AgentCheck.CRITICAL)


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
