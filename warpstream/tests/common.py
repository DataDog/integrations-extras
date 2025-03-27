# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.dev import get_docker_hostname

HOST = get_docker_hostname()

URL = 'http://{}:8080'.format(HOST)

INSTANCE = {'url': URL}

FULL_CONFIG = {
    'instances': [INSTANCE],
    'init_config': {},
}
