import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = 'http://{}:2020/api/v1/metrics/prometheus'.format(get_docker_hostname())
INSTANCE = {'prometheus_url': URL}


@pytest.fixture(scope='session')
def dd_environment_pass():
    compose_file = os.path.join(get_here(), 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(compose_file, endpoints=[URL]):
        yield INSTANCE


@pytest.fixture
def instance_pass():
    return INSTANCE.copy()