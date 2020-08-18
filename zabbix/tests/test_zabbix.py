import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.zabbix import ZabbixCheck


def test_check(aggregator, instance):
    instance = {}
    check = ZabbixCheck('zabbix', {}, [instance])

    with pytest.raises(ConfigurationError):
        check.check(instance)
