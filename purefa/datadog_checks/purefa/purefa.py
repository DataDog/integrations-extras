
from datadog_checks.base import OpenMetricsBaseCheckV2
from .metrics import METRIC_MAP


class PureFACheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "purefa"

    def __init__(self, name, init_config, instances):
        super(PureFACheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP]
            }
