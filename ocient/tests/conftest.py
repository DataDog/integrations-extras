import os

import pytest

from datadog_checks.dev import docker_run, get_here

from . import common

INSTANCE = {"openmetrics_endpoint": common.VECTOR_METRICS_URL}


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(get_here(), "docker/docker-compose.yaml")
    with docker_run(compose_file, endpoints=[common.VECTOR_METRICS_URL]):
        yield


@pytest.fixture(scope="session")
def instance():
    return INSTANCE
