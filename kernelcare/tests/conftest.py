import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here


@pytest.fixture(scope='session')
def dd_environment():

    compose_file = os.path.join(get_here(), 'docker', 'docker-compose.yml')

    KEY = 'Key'
    KEY_NOT_FOUND = 'Key-NotFound'
    LOGIN = 'Login'
    LOGIN_NOT_FOUND = 'Login-NotFound'
    API_TOKEN = 'ApiToken'
    API_TOKEN_NOT_FOUND = 'ApiToken-NotFound'

    URL = 'http://{}:8000/'.format(get_docker_hostname())

    endpoints = [
        URL + KEY,
        URL + KEY_NOT_FOUND,
        URL + LOGIN + '/' + API_TOKEN,
        URL + LOGIN_NOT_FOUND + '/' + API_TOKEN,
        URL + LOGIN + '/' + API_TOKEN_NOT_FOUND,
    ]

    with docker_run(compose_file, endpoints=endpoints):
        yield {
            'URL': URL,
            'KEY': KEY,
            'KEY_NOT_FOUND': KEY_NOT_FOUND,
            'LOGIN': LOGIN,
            'LOGIN_NOT_FOUND': LOGIN_NOT_FOUND,
            'API_TOKEN': API_TOKEN,
            'API_TOKEN_NOT_FOUND': API_TOKEN_NOT_FOUND,
        }
