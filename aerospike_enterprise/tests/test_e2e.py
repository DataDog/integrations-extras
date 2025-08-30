# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os

import pytest

from datadog_checks.aerospike_enterprise import AerospikeEnterpriseCheck
from datadog_checks.dev.utils import get_metadata_metrics

from .common import (
    ALL_METRICS,
    EXPECTED_PROM_EXPORTER_METRICS,
    EXPECTED_PROM_LATENCIES_METRICS,
    EXPECTED_PROM_NAMESPACE_METRICS,
    EXPECTED_PROM_NODE_STATS_METRICS,
    EXPECTED_PROM_SETS_METRICS,
    EXPECTED_PROM_SINDEX_METRICS,
    EXPECTED_PROM_SYSINFO_METRICS,
    HERE,
)

pytestmark = [pytest.mark.usefixtures("dd_environment"), pytest.mark.e2e]


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


@pytest.mark.e2e
def test_openmetrics_e2e(dd_agent_check, instance_openmetrics_v2):
    aggregator = dd_agent_check(instance_openmetrics_v2, rate=True)

    metric_to_check = EXPECTED_PROM_NAMESPACE_METRICS + EXPECTED_PROM_EXPORTER_METRICS
    metric_to_check = metric_to_check + EXPECTED_PROM_NODE_STATS_METRICS + EXPECTED_PROM_SETS_METRICS
    metric_to_check = metric_to_check + EXPECTED_PROM_LATENCIES_METRICS + EXPECTED_PROM_SINDEX_METRICS
    metric_to_check = metric_to_check + EXPECTED_PROM_SYSINFO_METRICS

    _test_metrics(
        aggregator,
        instance_openmetrics_v2,
        ALL_METRICS,
    )


def _test_metrics(
    aggregator,
    instance_openmetrics_v2,
    metrics_to_check,
):
    """
    checks validates all metrics and labels.
    """

    for metric_name in metrics_to_check:
        aggregator.assert_metric(metric_name)

        # no need to validate node-ticks for labels, as its a counter to check how many times exporter url is called
        #    node-ticks wiill not have any labels associated
        if metric_name not in ("aerospike.node.ticks", "aerospike.node.up"):
            aggregator.assert_metric_has_tag(
                metric_name,
                "endpoint:{}".format(instance_openmetrics_v2.get("openmetrics_endpoint")),
            )

            aggregator.assert_metric_has_tag_prefix(metric_name, "aerospike_cluster")
            aggregator.assert_metric_has_tag_prefix(metric_name, "aerospike_service")

            # latency metric should have le tag representing bucket
            # 1,2,4,8,16,32..., 65k
            if "aerospike.latencies" in metric_name and "_bucket" in metric_name:
                aggregator.assert_metric_has_tag_prefix(metric_name, "le")
