import os
import subprocess
from copy import deepcopy

import pytest

from datadog_checks.dev import docker_run, get_here
from datadog_checks.dev.conditions import WaitFor, CheckDockerLogs

from .common import BASE_CONFIG, CONTAINER_NAME, HOST, INVALID_URL, PASSWORD, USER, VALID_URL


@pytest.fixture(scope="session")
def dd_environment():
    """
    Spin up and initialize Nextcloud
    """
    compose_file = os.path.join(get_here(), 'compose', CONTAINER_NAME)
    with docker_run(
        compose_file=compose_file,
        env_vars={'NEXTCLOUD_ADMIN_USER': USER, 'NEXTCLOUD_ADMIN_PASSWORD': PASSWORD},
        conditions=[
            CheckDockerLogs(
                compose_file,
                [
                    "resuming normal operations",
                    "Initializing finished"
                ]
            ),
            WaitFor(nextcloud_container, attempts=15),
            WaitFor(nextcloud_install, attempts=15),
            WaitFor(nextcloud_add_trusted_domain, attempts=15),
            WaitFor(nextcloud_stats, attempts=15),
        ],
    ):
        yield BASE_CONFIG


@pytest.fixture
def instance():
    return BASE_CONFIG


@pytest.fixture
def empty_url_instance():
    empty_url_instance = deepcopy(BASE_CONFIG)
    empty_url_instance['url'] = ''
    return empty_url_instance


@pytest.fixture
def invalid_url_instance():
    invalid_url_instance = deepcopy(BASE_CONFIG)
    invalid_url_instance['url'] = INVALID_URL
    return invalid_url_instance


@pytest.fixture
def apps_stats_instance():
    instance = deepcopy(BASE_CONFIG)
    instance['apps_stats'] = True
    return instance


def nextcloud_container():
    """
    Wait for nextcloud to start
    """
    status_args = ['docker', 'exec', '--user', 'www-data', CONTAINER_NAME, 'php', 'occ', 'status']
    return subprocess.call(status_args) == 0


def nextcloud_install():
    """
    Wait for nextcloud to install
    """
    status_args = [
        'docker',
        'exec',
        '--user',
        'www-data',
        CONTAINER_NAME,
        'php',
        'occ',
        'maintenance:install',
        '-n',
        '--admin-user={}'.format(USER),
        '--admin-pass={}'.format(PASSWORD),
    ]
    return subprocess.call(status_args) == 0


def nextcloud_add_trusted_domain():
    """
    Wait for nextcloud to add container host to trusted domain
    """
    status_args = [
        'docker',
        'exec',
        '--user',
        'www-data',
        CONTAINER_NAME,
        'php',
        'occ',
        'config:system:set',
        'trusted_domains',
        '2',
        '--value={}'.format(HOST),
    ]
    return subprocess.call(status_args) == 0


def nextcloud_stats():
    """
    Wait for nextcloud monitoring endpoint to be reachable
    """
    status_args = ['curl', '-u', '{}:{}'.format(USER, PASSWORD), VALID_URL]
    return subprocess.call(status_args) == 0
