import os
import pytest
from datadog_checks.dev import docker_run
from . import common


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(
        os.path.join(common.HERE, 'docker', 'docker-compose.yaml'),
        endpoints=[common.METRICS_URL],
        sleep=10  # Give nginx time to start
    ):
        yield


@pytest.fixture
def instance():
    return {
        'url': 'http://localhost:8080',
        'username': 'test',
        'password': 'test'
    }
