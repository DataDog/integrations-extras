import os

import pytest
import requests

from datadog_checks.dev import WaitFor, docker_run, get_here
from datadog_checks.dev.conditions import CheckEndpoints

HERE = get_here()
COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')

INSTANCE = {'openmetrics_endpoint': 'http://localhost:2113/metrics'}


def create_subscription():
    response = requests.put(
        'http://localhost:2113/subscriptions/newstream/examplegroup',
        json={'startFrom': 0, 'resolveLinktos': False},
        timeout=10,
    )
    response.raise_for_status()


@pytest.fixture(scope='session')
def dd_environment():
    conditions = [
        CheckEndpoints(INSTANCE['openmetrics_endpoint']),
        WaitFor(create_subscription),
    ]
    with docker_run(COMPOSE_FILE, conditions=conditions):
        yield INSTANCE


@pytest.fixture
def instance():
    return dict(INSTANCE)
