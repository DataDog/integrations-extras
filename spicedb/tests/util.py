import os

from datadog_checks.dev import get_docker_hostname, get_here

HOST = get_docker_hostname()
PORT = '8080'

def get_fixture_path(filename):
    return os.path.join(get_here(), 'fixtures', filename)
