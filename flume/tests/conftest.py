import os

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.utils import load_jmx_config

from .common import HERE


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(HERE, 'compose', 'docker-compose.yml')
    patterns = [
        'Component type: CHANNEL, name: memchannel started',
        'Component type: CHANNEL, name: kafka-memchannel started',
        'Component type: SINK, name: hdfs-write started',
        'Component type: SINK, name: kafka-sink started',
        'Component type: SOURCE, name: hdfs-source started',
        'Component type: SOURCE, name: kafka-source started',
    ]
    with docker_run(compose_file, log_patterns=patterns):
        instance = load_jmx_config()
        yield instance, {'use_jmx': True}
