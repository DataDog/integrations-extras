from os import path

import pytest

from datadog_checks.dev import docker_run

from .common import (
    HERE,
    MOCK_INSTANCE_JSONRPC_AUTH,
    MOCK_INSTANCE_JSONRPC_NOAUTH,
    MOCK_INSTANCE_JSONRPC_REDIRECT,
    MOCK_INSTANCE_KAMCMD,
    MOCK_INSTANCE_MISSING_CONFIGS,
    MOCK_INSTANCE_USING_MMAPS,
)


@pytest.fixture(scope='session')
def dd_environment():
    instances = [
        MOCK_INSTANCE_USING_MMAPS.copy(),
        MOCK_INSTANCE_JSONRPC_NOAUTH.copy(),
        MOCK_INSTANCE_JSONRPC_AUTH.copy(),
        MOCK_INSTANCE_JSONRPC_REDIRECT.copy(),
        MOCK_INSTANCE_KAMCMD.copy(),
    ]

    with docker_run(compose_file=path.join(HERE, 'docker-env', 'docker-compose.yml'), sleep=10):
        yield instances


@pytest.fixture(scope='session')
def instance_missing_configs():
    return MOCK_INSTANCE_MISSING_CONFIGS.copy()


@pytest.fixture(scope='session')
def instance_using_mmaps():
    return MOCK_INSTANCE_USING_MMAPS.copy()


@pytest.fixture(scope='session')
def instance_jsonrpc_noauth():
    return MOCK_INSTANCE_JSONRPC_NOAUTH.copy()


@pytest.fixture(scope='session')
def instance_jsonrpc_auth():
    return MOCK_INSTANCE_JSONRPC_AUTH.copy()


@pytest.fixture(scope='session')
def instance_jsonrpc_redirect():
    return MOCK_INSTANCE_JSONRPC_REDIRECT.copy()


@pytest.fixture(scope='session')
def instance_kamcmd():
    return MOCK_INSTANCE_KAMCMD.copy()
