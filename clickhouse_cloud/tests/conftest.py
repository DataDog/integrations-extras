"""Shared test fixtures and mock setup for ClickHouse Cloud Datadog check tests.

The mock AgentCheck base class is injected into sys.modules here (rather than
inside individual test files) so that pytest guarantees it runs before any test
module is collected.  This avoids import-order issues when multiple test files
exist.
"""

import json
import os
import sys
from unittest.mock import MagicMock as _MagicMock

import pytest

# ---------------------------------------------------------------------------
# Mock AgentCheck base class
# ---------------------------------------------------------------------------


class MockAgentCheck:
    """Stand-in for datadog_checks.base.AgentCheck.

    Mimics the real API surface used by the check under test:
    - persistent cache (read/write)
    - send_log()
    - service_check(name, status, tags=None, message=None)
    - gauge(name, value, tags=None)
    - self.instance (set from instances[0])
    - self.log
    """

    OK = 0
    WARNING = 1
    CRITICAL = 2

    def __init__(self, name=None, init_config=None, instances=None):
        self._persistent_cache = {}
        self._sent_logs = []
        self._service_checks = []
        self._gauges = []
        self.log = _MagicMock()

        # The real AgentCheck sets self.instance = instances[0]
        if instances:
            self.instance = instances[0]
        else:
            self.instance = {}

    def read_persistent_cache(self, key):
        return self._persistent_cache.get(key)

    def write_persistent_cache(self, key, value):
        self._persistent_cache[key] = value

    def send_log(self, log_entry):
        self._sent_logs.append(log_entry)

    def service_check(self, name, status, tags=None, message=None):
        self._service_checks.append((name, status))

    def gauge(self, name, value, tags=None):
        self._gauges.append((name, value))


# ---------------------------------------------------------------------------
# Inject mock modules BEFORE any test file imports the check
# ---------------------------------------------------------------------------

_mock_agent_check_module = _MagicMock()
_mock_agent_check_module.AgentCheck = MockAgentCheck

# Only mock datadog_checks.base — leave datadog_checks itself as the real
# namespace package so that datadog_checks.clickhouse_cloud imports work.
sys.modules['datadog_checks.base'] = _mock_agent_check_module

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture
def query_log_rows():
    with open(os.path.join(FIXTURES_DIR, 'query_log_rows.json')) as f:
        return json.load(f)


@pytest.fixture
def text_log_rows():
    with open(os.path.join(FIXTURES_DIR, 'text_log_rows.json')) as f:
        return json.load(f)


@pytest.fixture
def default_instance():
    return {
        'service_id': 'test-service-uuid',
        'key_id': 'test-key-id',
        'key_secret': 'test-key-secret',
        'collect_query_logs': True,
        'collect_text_logs': True,
        'log_batch_size': 1000,
        'slow_query_threshold_ms': 5000,
        'initial_backfill_minutes': 60,
        'tags': ['env:test', 'clickhouse_cluster:test-cluster'],
    }
