# (C) Calastone Ltd. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
# System
import subprocess
import os
import time

# 3rd Party
import pytest

# Project
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
    instance = {'url': 'http://google.com'}
    with pytest.raises(CheckException):
        c.check(instance)

    # Decode Error
    instance = {'url': 'https://google.com'}
    with pytest.raises(CheckException):
        c.check(instance)


@pytest.fixture
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator


@pytest.mark.integration
def test_service_check(aggregator):
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

    HERE = os.path.dirname(os.path.abspath(__file__))
    args = [
        "docker-compose",
        "-f", os.path.join(HERE, 'docker-compose.yml')
    ]

    # start the Nginx container
    subprocess.check_call(args + ["up", "-d"])
    time.sleep(10)  # we should implement a better wait strategy :)

    # the check should send OK
    instance = {
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

    # stop the container
    subprocess.check_call(args + ["down"])
