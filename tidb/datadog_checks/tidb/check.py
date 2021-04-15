from datadog_checks.base import OpenMetricsBaseCheck

from .metrics import TIDB_METRICS, PD_METRICS, TIKV_METRICS, GO_RUNTIME_METRICS


class TiDBCheck(OpenMetricsBaseCheck):
    DEFAULT_METRIC_LIMIT = 0
    HEALTH_METRIC = 'tidb_cluster.up'

    def __init__(self, name, init_config, instances=None):
        default_ns = "tidb_cluster"

        default_metric_mappers = dict(TIDB_METRICS)
        default_metric_mappers.update(PD_METRICS)
        default_metric_mappers.update(TIKV_METRICS)
        default_metric_mappers.update(GO_RUNTIME_METRICS)

        default_instances = {
            'tidb-cluster': {
                'metrics': [default_metric_mappers],
                'send_distribution_sums_as_monotonic': 'true',
                'send_distribution_counts_as_monotonic': 'true',
                'send_distribution_buckets': 'true',
            }
        }

        super(TiDBCheck, self).__init__(
            name, init_config, instances, default_instances=default_instances, default_namespace=default_ns
        )

    # Override the process method to send the prometheus up metric, as service checks can be disabled.
    def process(self, scraper_config, metric_transformers=None):
        endpoint = scraper_config.get('prometheus_url')
        tags = ['instance:{}'.format(endpoint)]
        if scraper_config.get('custom_tags'):
            tags.extend(scraper_config.get('custom_tags'))

        try:
            super(TiDBCheck, self).process(scraper_config, metric_transformers=metric_transformers)
        except Exception:
            self.gauge(self.HEALTH_METRIC, 1, tags=tags)
            raise
        else:
            self.gauge(self.HEALTH_METRIC, 0, tags=tags)
