# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from .common import (
    ALL_METRICS,
    EXPECTED_PROM_EXPORTER_METRICS,
    EXPECTED_PROM_LATENCIES_METRICS,
    EXPECTED_PROM_NAMESPACE_METRICS,
    EXPECTED_PROM_NODE_STATS_METRICS,
    EXPECTED_PROM_SETS_METRICS,
    EXPECTED_PROM_SINDEX_METRICS,
    EXPECTED_PROM_SYSINFO_METRICS,
)


@pytest.mark.usefixtures("dd_environment")
def test_openmetrics_e2e(dd_agent_check, instance_openmetrics_v2):
    """
    check validates end-to-end metrics and labels.
    """
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
        if metric_name not in ("aerospike.server.node.ticks", "aerospike.server.node.up"):
            aggregator.assert_metric_has_tag(
                metric_name,
                "endpoint:{}".format(instance_openmetrics_v2.get("openmetrics_endpoint")),
            )

            aggregator.assert_metric_has_tag_prefix(metric_name, "aerospike_cluster")
            aggregator.assert_metric_has_tag_prefix(metric_name, "aerospike_service")

            # latency metric should have le tag representing bucket
            # 1,2,4,8,16,32..., 65k
            if "aerospike.server.latencies" in metric_name and "_bucket" in metric_name:
                aggregator.assert_metric_has_tag_prefix(metric_name, "le")
