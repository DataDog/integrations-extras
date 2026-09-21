import os

import pytest

from datadog_checks.dev import docker_run, get_here
from datadog_checks.dev.conditions import CheckDockerLogs, CheckEndpoints

HERE = get_here()
COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')

INSTANCE = {'openmetrics_endpoint': 'http://localhost:8080/metrics'}


@pytest.fixture(scope='session')
def dd_environment():
    conditions = [
        CheckDockerLogs(identifier='caddy', patterns=['server running']),
        CheckEndpoints(INSTANCE['openmetrics_endpoint']),
    ]
    with docker_run(COMPOSE_FILE, conditions=conditions):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE
