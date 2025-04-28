from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class Resilience4jCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "resilience4j"
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(Resilience4jCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {
            "metrics": [METRIC_MAP],
            "send_distribution_sums_as_monotonic": "true",
            "send_distribution_counts_as_monotonic": "true",
        }

    def check(self, _):
        super().check(_)
