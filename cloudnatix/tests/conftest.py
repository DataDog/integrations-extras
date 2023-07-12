import os

import pytest

from datadog_checks.dev import conditions, docker_run, get_here

from . import common


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker', 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(compose_file, conditions=[conditions.CheckEndpoints(common.METRICS_URL)]):
        yield {
            'openmetrics_endpoint': common.METRICS_URL,
        }


@pytest.fixture
def instance():
    return {
        'openmetrics_endpoint': common.METRICS_URL,
    }
