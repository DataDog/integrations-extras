import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.zabbix import ZabbixCheck


def test_empty_instance(aggregator, instance_empty):
    check = ZabbixCheck('zabbix', {}, [instance_empty])

    with pytest.raises(ConfigurationError):
        check.check(instance_empty)


def test_missing_pass(aggregator, instance_missing_pass):
    check = ZabbixCheck('zabbix', {}, [instance_missing_pass])

    with pytest.raises(ConfigurationError):
        check.check(instance_missing_pass)


def test_missing_url(aggregator, instance_missing_url):
    check = ZabbixCheck('zabbix', {}, [instance_missing_url])

    with pytest.raises(ConfigurationError):
        check.check(instance_missing_url)
