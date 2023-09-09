import os
from unittest import mock

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.upbound_uxp import UpboundUxpCheck

from . import common


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(
        common.COMPOSE_FILE,
        endpoints=[
            'http://{}:{}/metrics'.format(common.HOST, common.PORT),
        ],
    ):
        yield {"openmetrics_endpoint": 'http://{}:{}/metrics'.format(common.HOST, common.PORT)}


@pytest.fixture
def instance():
    print("conftest: instance")
    return {"verbose": False, "metrics_default": "min", "uxp_hosts": ["localhost"]}


@pytest.fixture
def check(instance):
    print("conftest: check")
    return UpboundUxpCheck({}, [instance])


@pytest.fixture()
def mock_metrics():
    print("conftest: mock_metrics")
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
