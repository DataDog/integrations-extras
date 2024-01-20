import os

import pytest

from datadog_checks.caddy import CaddyCheck
from datadog_checks.dev import docker_run, get_here

from .common import INSTANCE, METRICS_URL, MOCKED_INSTANCE

HERE = get_here()
COMPOSE_FILE = os.path.join(HERE, 'compose', 'docker-compose.yaml')


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(COMPOSE_FILE, endpoints=METRICS_URL, log_patterns="serving initial configuration"):
        yield {
            'instances': [INSTANCE],
        }


@pytest.fixture
def instance():
    return INSTANCE


@pytest.fixture
def mocked_instance():
    return MOCKED_INSTANCE


@pytest.fixture
def check():
    return lambda instance: CaddyCheck('caddy', {}, [instance])
