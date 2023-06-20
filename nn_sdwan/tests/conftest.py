# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

INSTANCE = {"hostname": "localhost", "username": "username", "password": "password", "protocol": "https"}


@pytest.fixture(scope='session')
def dd_environment():
    yield INSTANCE


@pytest.fixture(scope="session")
def instance_empty():
    instance = {}
    return instance


@pytest.fixture(scope="session")
def instance_normal():
    return INSTANCE.copy()


@pytest.fixture(scope="session")
def instance_missing_hostname():
    instance = INSTANCE.copy()
    del instance["hostname"]
    return instance


@pytest.fixture(scope="session")
def instance_missing_username():
    instance = INSTANCE.copy()
    del instance["username"]
    return instance


@pytest.fixture(scope="session")
def instance_missing_password():
    instance = INSTANCE.copy()
    del instance["password"]
    return instance


@pytest.fixture(scope="session")
def instance_missing_protocol():
    instance = INSTANCE.copy()
    del instance["protocol"]
    return instance


@pytest.fixture(scope="session")
def instance_e2e():
    return INSTANCE.copy()
