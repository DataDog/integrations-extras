import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.php_opcache import PhpOpcacheCheck

from .common import EXPECTED_METRICS


@pytest.mark.unit
def test_config():
    instance = {}
    c = PhpOpcacheCheck('php_opcache', {}, [instance])

    with pytest.raises(ConfigurationError):
        c.check(instance)

    c.check({'url': 'http://foobar'})


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = PhpOpcacheCheck('php_opcache', {}, [instance])

    c.check(instance)
    aggregator.assert_service_check('php_opcache.can_connect', PhpOpcacheCheck.OK)
    aggregator.reset()
    instance['url'] = instance['url'].replace('.php', '')
    c.check(instance)
    aggregator.assert_service_check('php_opcache.can_connect', PhpOpcacheCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_metrics(aggregator, instance):
    c = PhpOpcacheCheck('php_opcache', {}, [instance])

    c.check(instance)
    for k, v in EXPECTED_METRICS.items():
        aggregator.assert_metric(k, at_least=v)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)
