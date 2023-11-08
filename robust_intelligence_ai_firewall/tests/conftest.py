import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        'openmetrics_endpoint': 'http://localhost:8080/metrics'
    }
