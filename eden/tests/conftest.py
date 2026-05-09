import pytest

INSTANCE = {
    "url": "https://api.eden.example.com",
    "org_id": "TestOrg",
    "robot_username": "datadog-agent",
    "robot_api_key": "secret",
    "range_seconds": 300,
    "limit": 100,
}


@pytest.fixture
def instance():
    return INSTANCE.copy()
