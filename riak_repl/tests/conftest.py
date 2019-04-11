import pytest
import os

from datadog_checks.dev.conditions import CheckDockerLogs, CheckEndpoints
from datadog_checks.dev.docker import docker_run

from .common import HERE, URL


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(HERE, "docker", "docker-compose.yml")
    log_patterns = 'Full-sync with site "riak-west-1" completed'
    with docker_run(
        compose_file=compose_file,
        conditions=[CheckEndpoints(URL, wait=5), CheckDockerLogs(compose_file, log_patterns)],
    ):
        yield
