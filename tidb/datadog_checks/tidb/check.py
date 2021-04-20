from datadog_checks.base import OpenMetricsBaseCheck

from .metrics import GO_RUNTIME_METRICS, PD_METRICS, TIDB_METRICS, TIKV_METRICS


class TiDBCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):
        default_metrics = dict(TIDB_METRICS)
        default_metrics.update(PD_METRICS)
        default_metrics.update(TIKV_METRICS)
        default_metrics.update(GO_RUNTIME_METRICS)

        tidb_metrics = dict(TIDB_METRICS)
        tidb_metrics.update(GO_RUNTIME_METRICS)

        pd_metrics = dict(PD_METRICS)

        tikv_metrics = dict(TIKV_METRICS)

        default_instances = {
            'pd': {
                'prometheus_url': 'http://localhost:2379/metrics',
                'namespace': "pd",
                'metrics': [pd_metrics],
            },
            'tidb': {
                'prometheus_url': 'http://localhost:10080/metrics',
                'namespace': "tidb",
                'metrics': [tidb_metrics],
            },
            'tikv': {
                'prometheus_url': 'http://localhost:20180/metrics',
                'namespace': "tikv",
                'metrics': [tikv_metrics],
            },
            'tiflash_proxy': {
                'prometheus_url': 'http://localhost:20292/metrics',
                'namespace': "tiflash_proxy",
                'metrics': [default_metrics],
            },
            'tiflash': {
                'prometheus_url': 'http://localhost:8234/metrics',
                'namespace': "tiflash",
                'metrics': [default_metrics],
            },
            'ticdc': {
                'prometheus_url': 'http://localhost:8301/metrics',
                'namespace': "ticdc",
                'metrics': [default_metrics],
            },
            'dm_master': {
                'prometheus_url': 'http://localhost:8261/metrics',
                'namespace': "dm_master",
                'metrics': [default_metrics],
            },
            'dm_worker': {
                'prometheus_url': 'http://localhost:8262/metrics',
                'namespace': "dm_worker",
                'metrics': [default_metrics],
            },
            'pump': {
                'prometheus_url': 'http://localhost:8250/metrics',
                'namespace': "pump",
                'metrics': [default_metrics],
            },
        }

        # For the usage of instances and namespace,
        # see datadog_`checks.base.checks.openmetrics.mixins.OpenMetricsScraperMixin.create_scraper_configuration`
        super(TiDBCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace="tidb"
        )
