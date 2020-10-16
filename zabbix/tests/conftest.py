import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

HERE = get_here()
HOST = get_docker_hostname()

CONFIG = {
    'zabbix_user': 'Admin',
    'zabbix_password': 'zabbix',
    'zabbix_api': 'http://{}:8080/api_jsonrpc.php'.format(HOST),
}


@pytest.fixture(scope="session")
def dd_environment():
    with docker_run(
        compose_file=os.path.join(HERE, 'compose', 'docker-compose.yml'),
        sleep=20,
    ):
        yield CONFIG


@pytest.fixture(scope="session")
def instance_e2e():
    return CONFIG


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
