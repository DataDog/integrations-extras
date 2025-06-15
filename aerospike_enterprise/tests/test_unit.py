from copy import deepcopy

import pytest

from datadog_checks.aerospike_enterprise import AerospikeEnterpriseCheck
from datadog_checks.base import AgentCheck  # noqa: F401

from .common import (
    OPENMETRICS_V2_INSTANCE,
)


def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(OPENMETRICS_V2_INSTANCE)
    instance.pop("openmetrics_endpoint")

    check = AerospikeEnterpriseCheck(AerospikeEnterpriseCheck.__NAMESPACE__, {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check(f"{AerospikeEnterpriseCheck.__NAMESPACE__}.node.up", count=0)


@pytest.mark.integration
def test_metrics_warning(dd_run_check, instance_openmetrics_v2):
    instance_openmetrics_v2["metrics"] = ["migrate_rx_objs", "migrate_tx_objs"]
    check = AerospikeEnterpriseCheck(AerospikeEnterpriseCheck.__NAMESPACE__, {}, [instance_openmetrics_v2])

    with pytest.raises(Exception):
        dd_run_check(check)


@pytest.mark.e2e
def test_e2e(aggregator, dd_run_check):
    print("\t test_e2e -- aggregator", aggregator)
    assert True
