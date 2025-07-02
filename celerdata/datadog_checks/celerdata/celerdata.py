from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.celerdata.metrics import METRIC_MAP


class CelerdataCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'celerdata'

    def __init__(self, name, init_config, instances):
        super(CelerdataCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        """
        Returns the default OpenMetrics configuration.
        """
        return {
            'metrics': [METRIC_MAP],
            'exclude_metrics': [r'.*8060.*'],
        }
