import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.dev.conditions import CheckDockerLogs

HERE = get_here()
HOST = get_docker_hostname()

CONFIG = {
    'zabbix_user': 'Admin',
    'zabbix_password': 'zabbix',
    'zabbix_api': 'http://{}:8080/api_jsonrpc.php'.format(HOST),
}


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(HERE, 'compose', 'docker-compose.yml')
    with docker_run(
        compose_file=compose_file,
        sleep=120,
        conditions=[
            CheckDockerLogs(compose_file, 'php-fpm7.4 entered RUNNING state'),
        ],
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
