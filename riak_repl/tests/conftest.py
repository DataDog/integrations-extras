import pytest
import os

from datadog_checks.dev import docker_run

from .common import HERE


@pytest.fixture(scope="session")
def riak_server():
    with docker_run(
        compose_file=os.path.join(HERE, "docker", "docker-compose.yml"),
        sleep=30
    ):
        yield
