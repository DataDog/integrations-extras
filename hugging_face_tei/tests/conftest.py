import os
from unittest import mock

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.dev.conditions import CheckEndpoints
from datadog_checks.hugging_face_tei import HuggingFaceTeiCheck

HERE = get_here()
INSTANCE_URL = f"http://{get_docker_hostname()}:8080/metrics"


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(HERE, 'docker', 'docker-compose.yaml')
    conditions = [
        CheckEndpoints(INSTANCE_URL, attempts=120, wait=2),
    ]
    with docker_run(compose_file, conditions=conditions):
        instances = {'instances': [{'openmetrics_endpoint': INSTANCE_URL}]}
        yield instances


@pytest.fixture
def instance():
    return {
        'openmetrics_endpoint': INSTANCE_URL,
    }


@pytest.fixture
def check(instance):
    return HuggingFaceTeiCheck('hugging_face_tei', {}, [instance])


def mock_metrics_response(fixture_name):
    with open(os.path.join(HERE, 'fixtures', fixture_name), 'r') as f:
        content = f.read()

    return mock.patch(
        'requests.Session.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: content.split('\n'),
            headers={'Content-Type': 'text/plain'},
            close=lambda: None,
        ),
    )
