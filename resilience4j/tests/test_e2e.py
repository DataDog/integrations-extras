from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import assert_service_checks


def test_e2e_resilience4j(dd_agent_check, dd_environment):
    # pass
    aggregator = dd_agent_check()
    aggregator.assert_service_check('resilience4j.openmetrics.health', status=ServiceCheck.OK, count=1)
    assert_service_checks(aggregator)
