import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.dev.utils import get_metadata_metrics

from .common import ALL_METRICS

pytestmark = [pytest.mark.usefixtures("dd_environment"), pytest.mark.e2e]


@pytest.mark.e2e
def test_openmetrics_check(dd_agent_check, instance_openmetrics_v2):
    # Run the check inside the container
    aggregator = dd_agent_check(instance_openmetrics_v2, rate=True)

    # Construct tags (if any)
    tags = list(instance_openmetrics_v2.get("tags", []))
    tags.append("endpoint:" + instance_openmetrics_v2["openmetrics_endpoint"])

    # Service-check count will be 2 because aggregator scrapped the exporter twice to check rate metrics
    aggregator.assert_service_check("aerospike.openmetrics.health", AgentCheck.OK, tags=tags, count=2)

    # Validate all captured/expected metrics
    for metric in ALL_METRICS:
        aggregator.assert_metric(metric)

    # Final assertions
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
