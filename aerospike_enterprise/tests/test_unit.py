from copy import deepcopy

import pytest

from datadog_checks.aerospike_enterprise import AerospikeEnterpriseCheck
from datadog_checks.base import AgentCheck  # noqa: F401

from .common import (
    OPENMETRICS_V2_INSTANCE,
)


@pytest.mark.unit
def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(OPENMETRICS_V2_INSTANCE)
    instance.pop("openmetrics_endpoint")

    check = AerospikeEnterpriseCheck(AerospikeEnterpriseCheck.__NAMESPACE__, {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check(f"{AerospikeEnterpriseCheck.__NAMESPACE__}.node.up", count=0)
