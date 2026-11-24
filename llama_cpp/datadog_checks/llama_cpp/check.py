from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class LlamaCppCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'llama_cpp'
    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
        }
