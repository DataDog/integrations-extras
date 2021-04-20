import os

import pytest

from datadog_checks.dev.docker import docker_run

from .common import DOCKER_DIR, ENDPOINT, URL, registry_file_path

INSTANCE = {
    "stats_endpoint": ENDPOINT,
    "registry_file_path": registry_file_path("empty"),
}


@pytest.fixture(scope="session")
def dd_environment():

    with docker_run(os.path.join(DOCKER_DIR, "docker-compose.yaml"), endpoints=URL):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()
