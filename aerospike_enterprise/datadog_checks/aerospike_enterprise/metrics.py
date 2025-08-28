# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)


# We are using this to rename the metrics to datadog standard pattern
# keeping metric-type as gauge so new dasahboards are consistent with grafana dashboards already used by customers
METRIC_NAME_PATTERN = {
    r"^aerospike_(namespace)_(.*)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(node_stats)_(.*)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(sets)_(.*)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(sindex)_(.*)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(xdr)_(.*)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(sysinfo)_(.*)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(latencies)_(.*)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(node)_(up)$": {
        "metric_type": "gauge",
    },
    r"^aerospike_(node)_(ticks)$": {
        "metric_type": "gauge",
    },
}
