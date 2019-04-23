# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import os
import socket

import pytest

from datadog_checks.dev import docker_run, get_here, run_command
from datadog_checks.dev.conditions import WaitFor

from .common import HOST, INSTANCE


def wait_for_thrift():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, 6627))
    sock.close()


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'compose', 'docker-compose.yaml')

    # Build the topology jar to use in the environment
    with docker_run(compose_file, build=True, service_name='topology-maker', sleep=15):
        run_command(['docker', 'cp', 'topology-build:/topology.jar', os.path.join(get_here(), 'compose')])
    nimbus_condition = WaitFor(wait_for_thrift)
    with docker_run(compose_file, service_name='storm-nimbus', conditions=[nimbus_condition]):
        with docker_run(compose_file, service_name='storm-ui', log_patterns=[r'org.apache.storm.ui.core']):
            with docker_run(
                compose_file, service_name='topology', log_patterns=['Finished submitting topology: topology']
            ):
                yield INSTANCE
