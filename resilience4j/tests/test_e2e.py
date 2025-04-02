import pytest

from datadog_checks.dev.utils import get_metadata_metrics

from .common import EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.e2e]


# def test_resilience4j_e2e(dd_agent_check):
#     aggregator = dd_agent_check()
#     aggregator.assert_metrics_using_metadata(get_metadata_metrics())

#     for check in EXPECTED_PROMETHEUS_METRICS:
#         aggregator.assert_service_check(check)
