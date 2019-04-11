import os

import pytest

from datadog_checks.dev.docker import docker_run

from .common import DOCKER_DIR


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(os.path.join(DOCKER_DIR, 'docker-compose.yml')):
        yield {'ip_address': 'localhost', 'port': 161, 'community_string': 'public'}
