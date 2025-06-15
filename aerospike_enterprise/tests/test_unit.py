from copy import deepcopy

import pytest

from datadog_checks.aerospike_enterprise import AerospikeEnterpriseCheck
from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics

from .common import (
    ALL_METRICS,
    OPENMETRICS_V2_INSTANCE,
)


@pytest.mark.usefixtures('dd_environment')
@pytest.mark.e2e
def test_openmetrics_e2e(dd_agent_check, instance_openmetrics_v2):
    aggregator = dd_agent_check(instance_openmetrics_v2, rate=True)

    tags = "endpoint:" + instance_openmetrics_v2.get('openmetrics_endpoint')
    tags = instance_openmetrics_v2.get('tags').append(tags)

    aggregator.assert_service_check('aerospike.openmetrics.health', AgentCheck.OK, tags=tags)

    for metric in ALL_METRICS:
        aggregator.assert_metric(metric, tags=tags)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)


@pytest.mark.unit
def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(OPENMETRICS_V2_INSTANCE)
    instance.pop('openmetrics_endpoint')

    check = AerospikeEnterpriseCheck(AerospikeEnterpriseCheck.__NAMESPACE__, {}, [instance])

    try:
        dd_run_check(check)
    except Exception:
        assert True

    aggregator.assert_service_check(f'{AerospikeEnterpriseCheck.__NAMESPACE__}.node.up', count=0)
