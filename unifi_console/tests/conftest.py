import os

import pytest
from mock import patch
from tests.mocked_api import MockedAPI

from datadog_checks.unifi_console.unifi import Unifi


@pytest.fixture
def mock_api():
    with patch("datadog_checks.unifi_console.check.Unifi", MockedAPI):
        yield


@pytest.fixture
def mock___checkNewStyleAPI(monkeypatch):
    def mock_check(self):
        self.new = False

    with patch.object(Unifi, "_Unifi__checkNewStyleAPI", mock_check):
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
