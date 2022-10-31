import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {"url": "http://localhost", "access_token": "test"}
