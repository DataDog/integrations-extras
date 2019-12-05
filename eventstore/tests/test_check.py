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
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    init_config = {'metric_definitions': ALL_METRICS}

    c = EventStoreCheck('eventstore', init_config, {}, None)

    c.check(instance)

    for metric in init_config['metric_definitions']:
        aggregator.assert_metric(metric['metric_name'], tags=[])

    aggregator.assert_all_metrics_covered()
