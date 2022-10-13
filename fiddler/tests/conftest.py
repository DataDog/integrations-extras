import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "url": "https://junk.fiddler.ai",
        "fiddler_api_key": "api_key",
        "organization": "org_id",
    }
