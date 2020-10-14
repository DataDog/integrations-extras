import pytest


@pytest.fixture(scope="session")
def instance_empty():
    instance = {}
    return instance


@pytest.fixture(scope="session")
def instance_missing_pass():
    instance = {"zabbix_user": "zabbix"}
    return instance


@pytest.fixture(scope="session")
def instance_missing_url():
    instance = {"zabbix_user": "zabbix", "zabbix_password": "zabbix"}
    return instance
