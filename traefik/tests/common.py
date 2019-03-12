# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.dev import get_docker_hostname, get_here

HERE = get_here()
DOCKER_COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')
HOST = get_docker_hostname()
PORT = '8080'

INSTANCE = {
    'host': HOST,
    'port': PORT,
}

INSTANCE_BAD = {
    'host': 'foobar',
    'port': 9000,
}

INSTANCE_INVALID = {}
