import os

import mock
import pytest

from datadog_checks.dev import docker_run, get_here
from datadog_checks.dev.conditions import CheckDockerLogs
from datadog_checks.resilience4j.check import Resilience4jCheck

INSTANCE_URL = "http://localhost:9080/actuator/prometheus"
HERE = get_here()
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(DOCKER_DIR, 'docker-compose.yaml')

    with docker_run(compose_file, conditions=[CheckDockerLogs(compose_file, 'Finished resilience4j-demo tests')]):
        instances = {'instances': [{'prometheus_url': INSTANCE_URL}]}
        yield instances


@pytest.fixture
def instance():
    return {
        "prometheus_url": INSTANCE_URL,
    }


@pytest.fixture
def check(instance):
    return Resilience4jCheck("resilience4j", {}, [instance])


@pytest.fixture()
def mock_prometheus_metrics():
    fixture_file = os.path.join(os.path.dirname(__file__), "fixtures", "metrics-prometheus.txt")

    with open(fixture_file, "r") as f:
        content = f.read()

    with mock.patch(
        "requests.get",
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: content.split("\n"),
            headers={"Content-Type": "text/plain"},
        ),
    ):
        yield
