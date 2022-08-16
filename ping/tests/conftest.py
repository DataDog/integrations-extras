import pytest


@pytest.fixture(scope="session")
def dd_environment(instance):
    yield instance


@pytest.fixture(scope="session")
def instance_response_time():
    instance = {"host": "127.0.0.1", "collect_response_time": True, "tags": ["response_time:yes"]}
    return instance


@pytest.fixture(scope="session")
def instance():
    instance = {"host": "127.0.0.1", "tags": ["ping1", "ping2"]}
    return instance


@pytest.fixture(scope="session")
def instance_ipv6():
    instance = {"host": "0000:0000:0000:0000:0000:0000:0000:0001", "tags": ["ping1", "ping2"]}
    return instance


@pytest.fixture(scope="session")
def empty_instance():
    instance = {}
    return instance


@pytest.fixture(scope="session")
def incorrect_ip_instance():
    instance = {"host": "124.0.0.1"}
    return instance
