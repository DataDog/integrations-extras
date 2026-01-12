import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.dev.conditions import CheckDockerLogs
from datadog_checks.rundeck.check import RundeckCheck


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), "docker", "docker-compose.yaml")
    boot_condition = CheckDockerLogs(
        compose_file,
        r"Completed Rundeck initialization",
        attempts=60,  # long time to bootup
        wait=5,
    )

    with docker_run(compose_file, conditions=[boot_condition]):
        yield {"url": f"http://{get_docker_hostname()}:4440", "access_token": "my-static-token-123"}


@pytest.fixture
def instance():
    return {"url": f"http://{get_docker_hostname()}:4440", "access_token": "my-static-token-123"}


@pytest.fixture
def check(instance):
    return RundeckCheck("rundeck", {}, [instance])
