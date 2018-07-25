# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest
import os
import time

from datadog_checks.dev import docker_run

from .common import HERE


@pytest.fixture
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator


@pytest.fixture(scope="session")
def eventstore_server():
    with docker_run(compose_file=os.path.join(HERE, "compose", "docker-compose.yml")):
        time.sleep(10)  # we should implement a better wait strategy :)
        yield
