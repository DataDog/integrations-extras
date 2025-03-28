import os
from unittest.mock import MagicMock, patch

import mock
import pytest
from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.patroni import PatroniCheck

OPENMETRICS_ENDPOINT = "http://localhost:8888/metrics"
INSTANCE = {"openmetrics_endpoint": OPENMETRICS_ENDPOINT}


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(get_here(), "./docker/docker-compose.yaml")
    with docker_run(compose_file, endpoints=[OPENMETRICS_ENDPOINT]):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()


@pytest.fixture()
def mock_data():
    f_name = os.path.join(os.path.dirname(__file__), "fixtures", "metrics.txt")
    with open(f_name, "r") as f:
        text_data = f.read()
    with mock.patch(
        "requests.get",
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: text_data.split("\n"),
            headers={"Content-Type": "text/plain"},
        ),
    ):
        yield
