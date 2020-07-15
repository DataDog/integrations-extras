import pytest
import requests

from datadog_checks.base import ConfigurationError
from datadog_checks.base.errors import CheckException
from datadog_checks.kernelcare import KernelcareCheck


@pytest.mark.unit
def test_config():

    instance = {}
    c = KernelcareCheck('kernelcare', {}, [instance])

    with pytest.raises(ConfigurationError, match='^Configuration error.+'):
        c.check(instance)

    with pytest.raises(ConfigurationError, match='^Configuration error.+'):
        c.check({'key': ''})

    with pytest.raises(ConfigurationError, match='^Configuration error.+'):
        c.check({'login': '', 'api_token': ''})


@pytest.mark.integration
def test_metric(aggregator, dd_environment, monkeypatch):

    URL = dd_environment['URL']

    with monkeypatch.context() as m:
        m.setattr(KernelcareCheck, 'KEY_KCARE_NAGIOS_ENDPOINT', URL + '/notfound/', raising=True)
        instance = {'key': dd_environment['KEY']}
        c = KernelcareCheck('kernelcare', {}, [instance])
        with pytest.raises(requests.HTTPError):
            c.check(instance)

    aggregator.assert_service_check('kernelcare.can_connect', KernelcareCheck.CRITICAL)
    aggregator.reset()

    monkeypatch.setattr(KernelcareCheck, 'KEY_KCARE_NAGIOS_ENDPOINT', URL, raising=True)
    monkeypatch.setattr(KernelcareCheck, 'RES_KCARE_NAGIOS_ENDPOINT', URL, raising=True)

    instance = {'key': dd_environment['KEY_NOT_FOUND']}
    c = KernelcareCheck('kernelcare', {}, [instance])
    with pytest.raises(CheckException, match='^Servers not found for key.+'):
        c.check(instance)

    aggregator.assert_service_check('kernelcare.can_connect', KernelcareCheck.CRITICAL)
    aggregator.reset()

    instance = {'key': dd_environment['KEY']}
    c = KernelcareCheck('kernelcare', {}, [instance])
    c.check(instance)

    aggregator.assert_service_check('kernelcare.can_connect', KernelcareCheck.OK)
    aggregator.assert_metric('kernelcare.uptodate', value=6, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.outofdate', value=3, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.unsupported', value=2, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.inactive', value=1, metric_type=aggregator.GAUGE)
    aggregator.reset()

    instance = {'login': dd_environment['LOGIN_NOT_FOUND'], 'api_token': dd_environment['API_TOKEN']}
    c = KernelcareCheck('kernelcare', {}, [instance])
    with pytest.raises(CheckException, match='^Reseller not found$'):
        c.check(instance)

    instance = {'login': dd_environment['LOGIN'], 'api_token': dd_environment['API_TOKEN_NOT_FOUND']}
    c = KernelcareCheck('kernelcare', {}, [instance])
    with pytest.raises(CheckException, match='^Registration token not found for reseller.+'):
        c.check(instance)

    instance = {'login': dd_environment['LOGIN'], 'api_token': dd_environment['API_TOKEN']}
    c = KernelcareCheck('kernelcare', {}, [instance])
    c.check(instance)

    aggregator.assert_service_check('kernelcare.can_connect', KernelcareCheck.OK)
    aggregator.assert_metric('kernelcare.uptodate', value=9, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.outofdate', value=1, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.unsupported', value=3, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('kernelcare.inactive', value=2, metric_type=aggregator.GAUGE)
