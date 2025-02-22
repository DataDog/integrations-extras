import os

import pytest

from datadog_checks.dev.docker import docker_run, get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = get_docker_hostname()
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(os.path.join(DOCKER_DIR, 'docker-compose.yml'), log_patterns='Synchronization with replica'):
        yield


@pytest.fixture
def instance():
    return {'sentinel_host': HOST, 'sentinel_port': 26379, 'masters': ['mymaster']}
