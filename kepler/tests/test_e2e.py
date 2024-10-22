import pytest

from .conftest import EXPECTED_METRICS, INSTANCE


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    aggregator = dd_agent_check(INSTANCE)

    for metric in EXPECTED_METRICS:
        aggregator.assert_metric(metric, at_least=0)
