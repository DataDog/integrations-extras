import pytest

from datadog_checks.base import AgentCheck

pytestmark = [pytest.mark.e2e]


def test_e2e(dd_agent_check, aggregator, instance):

    with pytest.raises(Exception):
        dd_agent_check(instance, rate=True)
    aggregator.assert_service_check('resilience4j.openmetrics.health', AgentCheck.CRITICAL)
