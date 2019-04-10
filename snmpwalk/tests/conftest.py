import os

import pytest

from datadog_checks.dev.docker import docker_run

from .common import DOCKER_DIR, HOST


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(os.path.join(DOCKER_DIR, 'docker-compose.yml')):
        yield {'ip_address': HOST, 'port': 11111, 'community_string': 'public'}
