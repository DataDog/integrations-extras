from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class PureFBCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "purefb"

    DEFAULT_METRIC_LIMIT = 100000

    def __init__(self, name, init_config, instances):
        super(PureFBCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {
            "metrics": [METRIC_MAP],
            "openmetrics_endpoint": "http://localhost:9491/metrics/array?endpoint=array01",
        }
