from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.base.checks.openmetrics.v2.transform import NATIVE_TRANSFORMERS
from datadog_checks.cloudnatix.config_models import ConfigMixin

from .metrics import METRIC_MAP

GLOBAL_DB_NAME = 'global'


class CloudNatixCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = 'cloudnatix'

    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)

        self.cached_metric_data = {}
        self.check_initializations.append(self.configure_additional_transformers)

    def configure_transformer(self, metric_name):
        def custom_transformer(metric, sample_data, runtime_data):
            if metric.name in self.cached_metric_data:
                transformer = self.cached_metric_data[metric.name]
            else:
                transformer = NATIVE_TRANSFORMERS[metric.type](self, metric_name, {}, {})
                self.cached_metric_data[metric.name] = transformer

            transformer(metric, sample_data, runtime_data)

        return custom_transformer

    def configure_additional_transformers(self):
        metric_transformer = self.scrapers[self.config.openmetrics_endpoint].metric_transformer

        for raw_metric_name, metric_name in METRIC_MAP.items():
            metric_transformer.add_custom_transformer(
                f'.*?{raw_metric_name}$', self.configure_transformer(metric_name), pattern=True
            )
