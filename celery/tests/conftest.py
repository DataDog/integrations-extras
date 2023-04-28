# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest
from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckDockerLogs

from datadog_checks.celery import CeleryCheck
from .common import DOCKER_COMPOSE_PATH, REDIS_DB, REDIS_HOST, REDIS_PORT


@pytest.fixture(scope='session')
def dd_environment(worker_instance):
    with docker_run(
        DOCKER_COMPOSE_PATH,
        conditions=[
            CheckDockerLogs(DOCKER_COMPOSE_PATH,
                            ['Ready to accept connections', 'celery@worker ready'],
                            matches='all'),
        ]
    ):
        yield worker_instance


@pytest.fixture(scope='session')
def worker_instance():
    return {
        'app': 'tasks',
        'broker': f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        'remember_workers': True,
        'report_task_count': True,
        'report_rusage': True,
        'workers_crit_max': 5
    }


@pytest.fixture(scope='session')
def check():
    return lambda instance: CeleryCheck('celery', {}, [instance])
