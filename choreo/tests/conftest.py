import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

ENDPOINT = 'http://{}:9797'.format(get_docker_hostname()) + '/metrics'
INSTANCE = {'openmetrics_endpoint': ENDPOINT}


# Start a Docker container that runs a Flask program which serves a file containing Ballerina metrics. The purpose of
# this is to simulate the metrics endpoint of a Ballerina program. The metrics are served from a static file instead
# of a Ballerina program to ensure that the metrics report the same values always. This makes it possible to assert
# them in the tests.
@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'Docker/docker-compose.yaml')
    with docker_run(compose_file, endpoints=[ENDPOINT]):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE
