import os
import time
from urllib.request import urlopen

import pytest

from datadog_checks.dev import docker_run, get_here

from . import common


def wait_for_docker_ready():
    last_error = None
    for _ in range(100):
        try:
            urlopen(common.METRICS_URL)
            return
        except Exception as err:
            # wait and retry
            last_error = err
            time.sleep(0.1)
    raise last_error


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker', 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(compose_file):
        wait_for_docker_ready()
        yield


@pytest.fixture
def instance():
    return {
        'openmetrics_endpoint': common.METRICS_URL,
    }
