import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

INSTANCE = {
    "grpc_server_address": "{}:50051".format(get_docker_hostname()),
    "timeout": 1000,
    "rpc_header": ["want-health-check-response: SERVING"],
}


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(get_here(), "docker", "docker-compose.yml")
    with docker_run(compose_file):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()
