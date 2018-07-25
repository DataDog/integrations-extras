# (C) Calastone Ltd. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.eventstore import EventStoreCheck
from datadog_checks.errors import CheckException
from datadog_checks.utils.common import get_docker_hostname


def test_config():
    c = EventStoreCheck('eventstore', {}, {}, None)

    # empty instance
    instance = {}
    with pytest.raises(CheckException):
        c.check(instance)

    # Timeout
    instance = {'url': 'http://foobar'}
    with pytest.raises(CheckException):
        c.check(instance)

    # Statuscode
    instance = {'url': 'https://google.com/IwillReturnA404StatusCode'}
    with pytest.raises(CheckException):
        c.check(instance)

    # Decode Error
    instance = {'url': 'https://google.com'}
    with pytest.raises(CheckException):
        c.check(instance)


@pytest.mark.integration
def test_service_check(aggregator, eventstore_server):
    init_config = {
        'metric_definitions': [
            {
                'metric_type': 'gauge',
                'json_path': 'proc.mem',
                'json_type': 'int',
                'metric_name': 'eventstore.proc.mem'
            },
            {
                'metric_type': 'gauge',
                'json_path': 'proc.cpu',
                'json_type': 'float',
                'metric_name': 'eventstore.proc.cpu'
            },
            {
                'metric_type': 'gauge',
                'json_path': 'proc.tcp.measureTime',
                'json_type': 'datetime',
                'metric_name': 'eventstore.tcp.measure_time'
            }
        ]
    }

    c = EventStoreCheck('eventstore', init_config, {}, None)

    # the check should send OK
    instance = {
        'default_timeout': 5,
        'tag_by_url': True,
        'url': 'http://{}:2113/stats'.format(get_docker_hostname()),
        'name': 'testInstance',
        'json_path': [
            '*',
            '*.*',
            '*.*.*',
            '*.*.*.*'
        ]
    }
    c.check(instance)
    for metric in init_config['metric_definitions']:
        aggregator.assert_metric(metric['metric_name'], tags=[], count=1)

    # for m in aggregator.not_asserted():
    #     print(m)
    #
    # # Assert coverage for this check on this instance
    # aggregator.assert_all_metrics_covered()
