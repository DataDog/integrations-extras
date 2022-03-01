from datadog_checks.base import OpenMetricsBaseCheckV2, ConfigurationError

from .metrics import METRIC_MAP


class PureFACheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "purefa"

    DEFAULT_METRIC_LIMIT = 100000

    def __init__(self, name, init_config, instances):
        super(PureFACheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {
            "metrics": [METRIC_MAP],
            "openmetrics_endpoint": "http://localhost:9491/metrics/flasharray/array?endpoint=array01",
        }
