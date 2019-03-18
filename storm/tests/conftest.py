# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import os
from time import sleep

import pytest

from .common import INSTANCE
from datadog_checks.dev import docker_run, get_here, run_command


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'compose', 'docker-compose.yaml')

    # Build the topology jar to use in the environment
    with docker_run(compose_file, build=True, service_name='topology-maker'):
        sleep(15)
        run_command(
            ['docker', 'cp', 'topology-build:/topology.jar', os.path.join(get_here(), 'compose')]
        )

    with docker_run(compose_file, service_name='storm-ui',
                    log_patterns=[r'org.apache.storm.ui.core']):
        with docker_run(
            compose_file, service_name='topology',
            log_patterns=['Finished submitting topology: topology']
        ):
            yield INSTANCE
