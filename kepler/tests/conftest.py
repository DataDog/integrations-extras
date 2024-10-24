import os

import pytest

from datadog_checks.dev import docker_run, get_here
from datadog_checks.dev.conditions import CheckDockerLogs, CheckEndpoints

HERE = get_here()
COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')

INSTANCE = {'openmetrics_endpoint': 'http://localhost:8080/metrics'}

EXPECTED_METRICS = [
    'kepler.container.bpf_block_irq.count',
    'kepler.container.bpf_cpu_time.count',
    'kepler.container.bpf_net_rx_irq.count',
    'kepler.container.bpf_net_tx_irq.count',
    'kepler.container.bpf_page_cache_hit.count',
    'kepler.container.cache_miss.count',
    'kepler.container.core_joules.count',
    'kepler.container.cpu_cycles.count',
    'kepler.container.cpu_instructions.count',
    'kepler.container.dram_joules.count',
    'kepler.container.gpu_joules.count',
    'kepler.container.joules.count',
    'kepler.container.other_joules.count',
    'kepler.container.package_joules.count',
    'kepler.container.platform_joules.count',
    'kepler.container.task_clock.count',
    'kepler.container.uncore_joules.count',
    'kepler.node.core_joules.count',
    'kepler.node.dram_joules.count',
    'kepler.node.package_joules.count',
    'kepler.node.platform_joules.count',
    'kepler.node.uncore_joules.count',
    'kepler.node_info.count',
]


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = COMPOSE_FILE
    conditions = [
        CheckDockerLogs(identifier='caddy', patterns=['server running']),
        CheckEndpoints(INSTANCE["openmetrics_endpoint"]),
    ]
    with docker_run(compose_file, conditions=conditions):
        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE
