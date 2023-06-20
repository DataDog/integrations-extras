import time

import pytest
import requests
import simplejson as json
from mock import MagicMock, Mock

from datadog_checks.base import ConfigurationError
from datadog_checks.puma import PumaCheck


@pytest.mark.unit
def test_config(aggregator, instance):
    with pytest.raises(ConfigurationError):
        PumaCheck('puma', {}, [instance]).check({})


@pytest.mark.unit
def test_metrics_for_puma_in_cluster_mode(aggregator, instance):
    headers = {
        'server': 'FakeServer',
        'content-type': 'application/json',
    }
    content = json.dumps(
        {
            'workers': 2,
            'booted_workers': 2,
            'worker_status': [
                {
                    'last_status': {
                        'backlog': 0,
                        'max_threads': 20,
                        'pool_capacity': 15,
                        'running': 20,
                        'requests_count': 120,
                    }
                },
                {
                    'last_status': {
                        'backlog': 1,
                        'max_threads': 20,
                        'pool_capacity': 15,
                        'running': 20,
                        'requests_count': 150,
                    }
                },
            ],
        }
    )

    response = Mock(headers=headers, content=content)

    check = PumaCheck('puma', {}, [instance])
    check._perform_request = MagicMock(return_value=response)
    check.check({'control_url': "http://puma-control-url"})

    aggregator.assert_metric('puma.max_threads', value=40.0, tags=[])
    aggregator.assert_metric('puma.workers', value=2.0, tags=[])
    aggregator.assert_metric('puma.backlog', value=1.0, tags=[])
    aggregator.assert_metric('puma.booted_workers', value=2.0, tags=[])
    aggregator.assert_metric('puma.pool_capacity', value=30.0, tags=[])
    aggregator.assert_metric('puma.running', value=40.0, tags=[])
    aggregator.assert_metric('puma.requests_count', value=270.0, tags=[])
    aggregator.assert_service_check('puma.connection', PumaCheck.OK)


@pytest.mark.unit
def test_metrics_for_puma_in_single_mode(aggregator, instance):
    headers = {
        'server': 'FakeServer',
        'content-type': 'application/json',
    }

    content = json.dumps({"backlog": 1, "running": 2, "pool_capacity": 15, "max_threads": 20, "requests_count": 120})

    response = Mock(headers=headers, content=content)

    check = PumaCheck('puma', {}, [instance])
    check._perform_request = MagicMock(return_value=response)
    check.check({'control_url': "http://puma-control-url"})

    aggregator.assert_metric('puma.max_threads', value=20.0, tags=[])
    aggregator.assert_metric('puma.backlog', value=1.0, tags=[])
    aggregator.assert_metric('puma.pool_capacity', value=15.0, tags=[])
    aggregator.assert_metric('puma.running', value=2.0, tags=[])
    aggregator.assert_metric('puma.requests_count', value=120.0, tags=[])
    aggregator.assert_service_check('puma.connection', PumaCheck.OK)

    # This behaviour does not bring any value only extra cost, will always be 0 in single mode.
    aggregator.assert_metric('puma.workers', value=0.0, tags=[])
    aggregator.assert_metric('puma.booted_workers', value=0.0, tags=[])


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check(aggregator, instance, test_server):
    time.sleep(10)

    requests.get(test_server)

    time.sleep(5)

    check = PumaCheck('puma', {}, {}, None)
    check.check(instance)

    aggregator.assert_metric('puma.max_threads', value=10.0, tags=[])
    aggregator.assert_metric('puma.workers', value=2.0, tags=[])
    aggregator.assert_metric('puma.backlog', value=0.0, tags=[])
    aggregator.assert_metric('puma.booted_workers', value=2.0, tags=[])
    aggregator.assert_metric('puma.pool_capacity', value=10.0, tags=[])
    aggregator.assert_metric('puma.running', value=10.0, tags=[])
    aggregator.assert_metric('puma.requests_count', value=1.0, tags=[])
    aggregator.assert_service_check('puma.connection', PumaCheck.OK)
