import os
from unittest import mock

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.gitea import GiteaCheck


@pytest.fixture(scope="session")
def dd_environment():
    url = f"http://{get_docker_hostname()}:3000/metrics"
    instance = {"openmetrics_endpoint": url}

    compose_file = os.path.join(get_here(), "docker/docker-compose.yaml")
    with docker_run(compose_file, endpoints=[url]):
        yield instance


@pytest.fixture
def instance():
    return {
        "openmetrics_endpoint": "http://localhost:3000/metrics",
    }


@pytest.fixture
def check(instance):
    return GiteaCheck("gitea", {}, [instance])


@pytest.fixture()
def mock_metrics():
    fixture_file = os.path.join(os.path.dirname(__file__), "fixtures", "metrics.txt")

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
