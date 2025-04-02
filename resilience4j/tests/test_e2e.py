import pytest

from .common import EXPECTED_PROMETHEUS_METRICS, INSTANCE

pytestmark = [pytest.mark.e2e]


CONFIG = {
    "init_config": {},
    "instances": [INSTANCE],
}


def test_resilience4j_e2e(dd_agent_check):
    aggregator = dd_agent_check()
    aggregator.assert_metric(f"resilience4j.{EXPECTED_PROMETHEUS_METRICS[0]}")
