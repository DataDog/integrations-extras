import pytest

from datadog_checks.checks import AgentCheck
from datadog_checks.ping import PingCheck
from datadog_checks.errors import CheckException


def test_check(aggregator, instance):
    c = PingCheck('ping', {}, {})

    # empty instance
    instance = {}
    with pytest.raises(CheckException):
        c.check(instance)

    # only name
    with pytest.raises(CheckException):
        c.check({'name': 'Datadog'})

    # good check
    instance = {
        'host': '127.0.0.1',
        'name': "Localhost"
    }
    c.check(instance)
    aggregator.assert_service_check('network.ping.can_connect', AgentCheck.OK)

    # bad check
    instance = {
        'host': '192.0.2.0',
        'name': "Reserved IP"
    }
    c.check(instance)
    aggregator.assert_service_check('network.ping.can_connect', AgentCheck.CRITICAL)
