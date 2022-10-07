import os

import pytest
from mock import patch
from tests.mocked_api import MockedAPI


@pytest.fixture
def mock_api():
    with patch("datadog_checks.unifi_console.check.UnifiAPI", MockedAPI):
        yield


@pytest.fixture(scope="session")
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "url": os.environ.get("UNIFi_URL", "https://FAKE"),
        "user": os.environ.get("UNIFi_USER", "FAKE"),
        "pwd": os.environ.get("UNIFi_PWD", "FAKE"),
        "version": os.environ.get("UNIFI_VERSION", "v7"),
        "empty_default_hostname": True,
        "persist_connections": True,
    }
