import os

from datadog_checks.dev.docker import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = get_docker_hostname()
DOCKER_DIR = os.path.join(HERE, 'docker')
