import pytest


@pytest.fixture(scope='session')
def dd_environment(instance):
    yield instance


@pytest.fixture(scope='session')
def instance():
    return {"url": "https://demo.trial.fiddler.ai", "fiddler_api_key": "apikey", "organization": "demo"}
