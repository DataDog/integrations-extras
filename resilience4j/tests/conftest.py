import os
from unittest import mock

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.dev.conditions import CheckDockerLogs, CheckEndpoints
from datadog_checks.resilience4j.check import Resilience4jCheck

# Constants setup
INSTANCE_URL = f"http://{get_docker_hostname()}:9080/actuator/prometheus"
HERE = get_here()
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    """
    Fixture to manage the Docker test environment.
    It sets up the Docker environment using a compose file,
    waits until the application is ready, and cleans up afterward.
    """
    compose_file = os.path.join(DOCKER_DIR, 'docker-compose.yaml')
    conditions = [
        CheckDockerLogs(identifier="tester", patterns=["Finished resilience4j-demo tests"]),
        CheckEndpoints(INSTANCE_URL, attempts=120, wait=2),
    ]
    # Start the Docker environment and yield instances
    with docker_run(compose_file, sleep=5, conditions=conditions):
        instances = {'instances': [{'openmetrics_endpoint': INSTANCE_URL}]}
        yield instances


@pytest.fixture
def instance():
    """
    Returns a single instance configuration for the Resilience4j check.
    """
    return {
        "openmetrics_endpoint": INSTANCE_URL,
    }


@pytest.fixture
def check(instance):
    """
    Returns a check instance for Resilience4j.
    This allows isolated testing of the check logic.
    """
    return Resilience4jCheck("resilience4j", {}, [instance])


@pytest.fixture()
def mock_prometheus_metrics():
    """
    Mocks Prometheus metrics by simulating the response from the server.
    Reads metrics data from the fixture file fixtures/metrics-prometheus.txt.
    """
    # Path to the fixture file
    fixture_file = os.path.join(os.path.dirname(__file__), "fixtures", "metrics-prometheus.txt")
    # Attempt to open and read the fixture file, handle errors gracefully
    try:
        with open(fixture_file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        pytest.fail(f"Metrics fixture file not found: {fixture_file}")
    except Exception as e:
        pytest.fail(f"Error reading metrics fixture file: {fixture_file}. Error: {e}")
    # Mock requests.get method to simulate Prometheus response
    with mock.patch(
        "requests.get",
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: content.split("\n"),
            headers={"Content-Type": "text/plain"},
        ),
    ):
        yield
