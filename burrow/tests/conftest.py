import pytest
import os

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = "http://{}:8000".format(get_docker_hostname())
INSTANCE = {"url": URL, "clusters": "local"}


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(get_here(), "docker-compose.yaml")

    with docker_run(compose_file, endpoints=[URL]):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()
