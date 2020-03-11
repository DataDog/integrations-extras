# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os

import pytest

from datadog_checks.dev import docker_run

from .common import HERE, HOST, PORT


@pytest.fixture(scope="session")
def dd_environment(instance):
    with docker_run(compose_file=os.path.join(HERE, "compose", "docker-compose.yml"), sleep=60):
        yield instance


@pytest.fixture(scope='session')
def instance():
    return {
        'default_timeout': 5,
        'tag_by_url': True,
        'url': 'http://{}:{}'.format(HOST, PORT),
        'endpoints': ['/stats', '/info', '/projections/all-non-transient', '/subscriptions', '/gossip'],
        'name': 'testInstance',
        'json_path': ['*', '*.*', '*.*.*', '*.*.*.*'],
        'user': 'admin',
        'password': 'changeit',
    }
