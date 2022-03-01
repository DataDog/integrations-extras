
from datadog_checks.base import OpenMetricsBaseCheckV2, ConfigurationError
from .metrics import METRIC_MAP


class PureFACheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "purefa"

    DEFAULT_METRIC_LIMIT = 100000

    def __init__(self, name, init_config, instances):
        super(PureFACheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
            'openmetrics_endpoint': "http://localhost:9491/metrics/flasharray/array?endpoint=array01",
            'hostname_label': "host",
            'hostname_format': "<HOSTNAME>",
            'min_collection_interval': "120",
            'empty_default_hostname': True
            }

    def check(self, instance):
        endpoint = instance.get('openmetrics_endpoint')
        if endpoint is None:
            raise ConfigurationError("Unable to find openmetrics_endpoint in config file.")

        super().check(instance)
