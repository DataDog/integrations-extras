import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "url": "https://demo.fiddler.ai",
        "fiddler_api_key": "K4ph7ORDcIO2xVIEA6KxL1o1zHjZockgurhCOZOUSVs",
        "organization": "demo",
    }
