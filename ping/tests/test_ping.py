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


def test_check(aggregator, instance):
    c = PingCheck('ping', {}, {})

    # empty instance
    instance = {}
    with pytest.raises(CheckException):
        c.check(instance)

    # only name
    with pytest.raises(CheckException):
        c.check({'name': 'Datadog'})

    test_check
    # good check
    instance = {
        'host': '127.0.0.1',
        'name': "Localhost"
    }

    with mock.patch.object(c, "_exec_ping", return_value=mock_exec_ping()):
        c.check(instance)
    aggregator.assert_service_check('network.ping.can_connect', AgentCheck.OK)
