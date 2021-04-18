from datadog_checks.base import OpenMetricsBaseCheck

from .metrics import TIDB_METRICS, PD_METRICS, TIKV_METRICS, GO_RUNTIME_METRICS


class TiDBCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):
        default_ns = "tidb_cluster"

        default_metric_mappers = dict(TIDB_METRICS)
        default_metric_mappers.update(PD_METRICS)
        default_metric_mappers.update(TIKV_METRICS)
        default_metric_mappers.update(GO_RUNTIME_METRICS)

        default_instances = {
            'pd': {'prometheus_url': 'http://localhost:2379/metrics'},
            'tidb': {'prometheus_url': 'http://localhost:10080/metrics'},
            'tikv': {'prometheus_url': 'http://localhost:20180/metrics'},
            'tiflash_proxy': {'prometheus_url': 'http://localhost:20292/metrics'},
            'tiflash': {'prometheus_url': 'http://localhost:8234/metrics'},
            'ticdc': {'prometheus_url': 'http://localhost:8301/metrics'},
            'dm_master': {'prometheus_url': 'http://localhost:8261/metrics'},
            'dm_worker': {'prometheus_url': 'http://localhost:8262/metrics'},
            'pump': {'prometheus_url': 'http://localhost:8250/metrics'},
        }

        for name, instance in default_instances.iteritems():
            default_conf = {
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            }
            default_instances[name] = instance.update(default_conf)

        super(TiDBCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace=default_ns
        )
