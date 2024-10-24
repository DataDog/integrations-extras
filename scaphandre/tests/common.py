# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.dev import get_here

HERE = get_here()
COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker_compose.yaml')

METRICS = {
    'host.power',
    'process.power_consumption',
    'host.energy.count',
    'host.swap.total',
    'host.swap.free',
    'host.memory.free',
    'host.memory.available',
    'host.memory.total',
    'host.disk.total',
    'host.disk.available',
    'host.cpu.frequency',
    'host.load.avg.15',
    'host.load.avg.5',
    'host.load.avg.1',
    'self.memory',
    'self.memory.virtual',
    'self.topo_stats',
    'self.topo_records',
    'self.topo_procs',
    'self.socket_stats',
    'self.socket_records',
    'process.cpu_usage.pct',
    'process.memory',
    'process.memory.virtual',
    'process.disk.total_write',
    'process.disk.write',
    'process.disk.read',
    'process.disk.total_read',
    'version'
}

MOCKED_INSTANCE = {
    'openmetrics_endpoint': 'http://localhost:8080/metrics',
}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
