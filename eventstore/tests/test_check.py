# (C) Calastone Ltd. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.eventstore import ALL_METRICS, EventStoreCheck


def test_config():
    c = EventStoreCheck('eventstore', {}, {}, None)

    # empty instance
    instance = {}
    with pytest.raises(CheckException):
        c.check(instance)

    # empty list of metric endpoints
    instance = {'url': 'http://foobar', 'endpoints': []}
    with pytest.raises(CheckException, match='.+is empty$'):
        c.check(instance)

    # bad list of metric endpoints
    instance = {'url': 'http://foobar', 'endpoints': 'baz'}
    with pytest.raises(CheckException, match='^Incorrect value.+'):
        c.check(instance)

    # unknown metric endpoint
    instance = {'url': 'http://foobar', 'endpoints': ['/quux']}
    with pytest.raises(CheckException, match='^Unknown.+'):
        c.check(instance)

    # Timeout
    instance = {'url': 'http://10.0.0.0', 'endpoints': ['/stats']}
    with pytest.raises(CheckException, match='.+timed out.+'):
        c.check(instance)

    # Statuscode
    instance = {'url': 'https://google.com/IwillReturnA404StatusCode', 'endpoints': ['/stats']}
    with pytest.raises(CheckException, match='^Invalid Status Code.+'):
        c.check(instance)

    # Decode Error
    c = EventStoreCheck('eventstore', {'metric_definitions': {'/': []}}, {}, None)
    instance = {'url': 'https://google.com', 'endpoints': ['/']}
    with pytest.raises(CheckException, match='.+unserializable.+'):
        c.check(instance)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    init_config = {'metric_definitions': ALL_METRICS}

    c = EventStoreCheck('eventstore', init_config, {}, None)

    c.check(instance)

    for metric_definitions in init_config['metric_definitions'].values():
        for metric in metric_definitions:
            aggregator.assert_metric(metric['metric_name'], tags=[])

    aggregator.assert_all_metrics_covered()
