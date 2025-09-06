# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os
from copy import deepcopy

import pytest

from datadog_checks.aerospike_enterprise import AerospikeEnterpriseCheck
from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics

from .common import HERE, OPENMETRICS_V2_INSTANCE


def get_fixture_path(filename):
    return os.path.join(HERE, "fixtures", filename)


def test_openmetricsv2_check(aggregator, dd_run_check, instance_openmetrics_v2, mock_http_response):
    """
    check validates, mock prom metrics and metadata.csv
    """

    check = AerospikeEnterpriseCheck(AerospikeEnterpriseCheck.__NAMESPACE__, {}, [instance_openmetrics_v2])
    dd_run_check(check)

    mock_http_response(file_path=get_fixture_path("prometheus.txt"))

    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)


def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(OPENMETRICS_V2_INSTANCE)
    instance.pop("openmetrics_endpoint")

    check = AerospikeEnterpriseCheck(AerospikeEnterpriseCheck.__NAMESPACE__, {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check(f"{AerospikeEnterpriseCheck.__NAMESPACE__}.node.up", count=0)
