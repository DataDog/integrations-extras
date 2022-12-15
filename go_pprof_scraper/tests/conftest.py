# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = "http://{}:8888/debug/pprof/".format(get_docker_hostname())
INSTANCE = {
    "pprof_url": URL,
    "profiles": ["heap"],
    "tags": ["foo:bar"],
    "service": "testing",
    "duration": 1,
    "min_collection_interval": 5,
}


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(get_here(), "docker", "docker-compose.yml")

    # We need to enable the trace-agent for testing since it won't be enabled by
    # default
    agent_env_vars = {"DD_APM_PROFILING_DD_URL": "http://localhost:9999/profiles", "DD_APM_ENABLED": "true"}
    with docker_run(
        compose_file,
        endpoints=[URL],
        build=True,
    ):
        # According to
        # https://datadoghq.dev/integrations-core/ddev/plugins/#environment-manager
        # we can yield two dictionaries here, where the second one will be
        # configuration for the agent. We need this so we can start the trace
        # agent since it's off by default
        yield INSTANCE, dict(env_vars=agent_env_vars)


@pytest.fixture
def instance():
    return INSTANCE
