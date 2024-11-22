import os

import pytest

from datadog_checks.dev import docker_run, get_here
from datadog_checks.dev.conditions import CheckDockerLogs, CheckEndpoints

HERE = get_here()
COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')

INSTANCE = {'openmetrics_endpoint': 'http://localhost:8080/metrics'}

EXPECTED_METRICS = [
    'kepler.container.usage.bpf_block_irq.count',
    'kepler.container.usage.bpf_cpu_time.count',
    'kepler.container.usage.bpf_net_rx_irq.count',
    'kepler.container.usage.bpf_net_tx_irq.count',
    'kepler.container.usage.bpf_page_cache_hit.count',
    'kepler.container.usage.cache_miss.count',
    'kepler.container.usage.core_joules.count',
    'kepler.container.usage.cpu_cycles.count',
    'kepler.container.usage.cpu_instructions.count',
    'kepler.container.usage.dram_joules.count',
    'kepler.container.usage.gpu_joules.count',
    'kepler.container.usage.joules.count',
    'kepler.container.usage.other_joules.count',
    'kepler.container.usage.package_joules.count',
    'kepler.container.usage.platform_joules.count',
    'kepler.container.usage.task_clock.count',
    'kepler.container.usage.uncore_joules.count',
    'kepler.node.usage.core_joules.count',
    'kepler.node.usage.dram_joules.count',
    'kepler.node.usage.package_joules.count',
    'kepler.node.usage.platform_joules.count',
    'kepler.node.usage.uncore_joules.count',
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
