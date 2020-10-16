import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

CONTROL_URL = 'http://{}:19293/stats?token=12345'.format(get_docker_hostname())
INSTANCE = {'control_url': CONTROL_URL}
TEST_SERVER_URL = 'http://{}:30001/'.format(get_docker_hostname())


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker', 'docker-compose.yml')

    with docker_run(compose_file, endpoints=[CONTROL_URL]):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()


@pytest.fixture
def test_server():
    return TEST_SERVER_URL
