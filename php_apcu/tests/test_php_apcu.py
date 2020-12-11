import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.php_apcu import PhpApcuCheck

from .common import EXPECTED_METRICS


@pytest.mark.unit
def test_config():
    instance = {}
    c = PhpApcuCheck('php_apcu', {}, [instance])

    with pytest.raises(ConfigurationError):
        c.check(instance)

    c.check({'url': 'http://foobar'})


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = PhpApcuCheck('php_apcu', {}, [instance])

    c.check(instance)
    aggregator.assert_service_check('php_apcu.can_connect', PhpApcuCheck.OK)

    instance['url'] = instance['url'].replace('.php', '')
    c.check(instance)
    aggregator.assert_service_check('php_apcu.can_connect', PhpApcuCheck.CRITICAL)


def test_metrics(aggregator, instance):
    c = PhpApcuCheck('php_apcu', {}, [instance])

    c.check(instance)
    for k, v in EXPECTED_METRICS.items():
        aggregator.assert_metric(k, at_least=v)

    aggregator.assert_all_metrics_covered()
