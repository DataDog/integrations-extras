import pytest
import os

from datadog_checks.dev.conditions import CheckEndpoints
from datadog_checks.dev.docker import docker_run

from .common import HERE, URL


@pytest.fixture(scope="session")
def dd_environment():
    with docker_run(
        compose_file=os.path.join(HERE, "docker", "docker-compose.yml"),
        conditions=[CheckEndpoints(URL, wait=5)],
        sleep=60
    ):
        yield
