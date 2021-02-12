import os

import mock
import pytest

from datadog_checks.dev import docker_run, get_here
from datadog_checks.octoprint.check import BED_URL, EXTRUDER_URL, JOB_URL

from .common import (
    INSTANCE,
    MOCK_ACTIVE_JOB_RESPONSE,
    MOCK_BED_RESPONSE,
    MOCK_EMPTY_JOB_RESPONSE,
    MOCK_EXTRUDER_RESPONSE,
    URL,
)


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker-compose.yml')
    with docker_run(compose_file, endpoints=[URL]):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()


@pytest.fixture
def mock_empty_api_request():
    api_mock = get_api_mock('empty')
    with mock.patch('requests.get', new=api_mock):
        yield


@pytest.fixture
def mock_active_api_request():
    api_mock = get_api_mock('active')
    with mock.patch('requests.get', new=api_mock):
        yield


def get_api_mock(job_type):
    if job_type == 'empty':
        job_response = MOCK_EMPTY_JOB_RESPONSE
    else:
        job_response = MOCK_ACTIVE_JOB_RESPONSE

    def requests_get_mock(url, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

            def raise_for_status(self):
                return True

        if url.endswith(JOB_URL):
            return MockResponse(job_response, 200)

        elif url.endswith(EXTRUDER_URL):
            return MockResponse(MOCK_EXTRUDER_RESPONSE, 200)

        elif url.endswith(BED_URL):
            return MockResponse(MOCK_BED_RESPONSE, 200)

    return requests_get_mock
