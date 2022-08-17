import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {"url": "https://demo.trial.fiddler.ai", "fiddler_api_key": "apikey", "organization": "demo"}
