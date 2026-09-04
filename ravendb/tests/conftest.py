import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.dev.conditions import CheckEndpoints
from datadog_checks.ravendb import RavendbCheck

INSTANCE_URL = f"http://{get_docker_hostname()}:8080/admin/monitoring/v1/prometheus"
HERE = get_here()
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    if not os.getenv("RAVEN_License"):
        yield
        return

    compose_file = os.path.join(DOCKER_DIR, 'docker-compose.yaml')
    conditions = [
        CheckEndpoints(INSTANCE_URL, attempts=120, wait=2),
    ]

    with docker_run(
        compose_file, sleep=5, conditions=conditions, env_vars={"RAVEN_License": os.environ["RAVEN_License"]}
    ):
        instances = {'instances': [{'openmetrics_endpoint': INSTANCE_URL}]}
        yield instances


@pytest.fixture
def instance():
    return {
        "openmetrics_endpoint": INSTANCE_URL,
    }


@pytest.fixture
def check(instance):
    return RavendbCheck("ravendb", {}, [instance])
