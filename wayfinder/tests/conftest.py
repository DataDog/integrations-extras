import os
from unittest import mock

import pytest

from datadog_checks.wayfinder import WayfinderCheck


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "openmetrics_endpoint": "http://localhost:9090",
    }


@pytest.fixture
def check(instance):
    return WayfinderCheck("wayfinder", {}, [instance])


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
