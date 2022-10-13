import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "url": "REPLACE_WITH_URL",
        "fiddler_api_key": "REPLACE_WITH_API_KEY",
        "organization": "REPLACE_WITH_ORG_ID",
    }
