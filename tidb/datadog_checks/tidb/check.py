from datadog_checks.base import OpenMetricsBaseCheck

from .metrics import TIDB_METRICS, PD_METRICS, TIKV_METRICS, GO_RUNTIME_METRICS


class TiDBCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):
        default_metric_mappers = dict(TIDB_METRICS)
        default_metric_mappers.update(PD_METRICS)
        default_metric_mappers.update(TIKV_METRICS)
        default_metric_mappers.update(GO_RUNTIME_METRICS)

        default_instances = {
            'pd': {
                'prometheus_url': 'http://localhost:2379/metrics',
                'namespace': "pd",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'tidb': {
                'prometheus_url': 'http://localhost:10080/metrics',
                'namespace': "tidb",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'tikv': {
                'prometheus_url': 'http://localhost:20180/metrics',
                'namespace': "tikv",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'tiflash_proxy': {
                'prometheus_url': 'http://localhost:20292/metrics',
                'namespace': "tiflash_proxy",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'tiflash': {
                'prometheus_url': 'http://localhost:8234/metrics',
                'namespace': "tiflash",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'ticdc': {
                'prometheus_url': 'http://localhost:8301/metrics',
                'namespace': "ticdc",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'dm_master': {
                'prometheus_url': 'http://localhost:8261/metrics',
                'namespace': "dm_master",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'dm_worker': {
                'prometheus_url': 'http://localhost:8262/metrics',
                'namespace': "dm_worker",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
            'pump': {
                'prometheus_url': 'http://localhost:8250/metrics',
                'namespace': "pump",
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': True,
                'send_distribution_counts_as_monotonic': True,
                'send_distribution_buckets': True,
            },
        }

        ## For the usage of instances and namespace, see datadog_`checks.base.checks.openmetrics.mixins.OpenMetricsScraperMixin.create_scraper_configuration`
        super(TiDBCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace="tidb"
        )
