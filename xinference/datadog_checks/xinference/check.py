from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class XinferenceCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'xinference'
    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
        }
