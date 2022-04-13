import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {"url": "http://localhost/rest/", "api_key": ""}
