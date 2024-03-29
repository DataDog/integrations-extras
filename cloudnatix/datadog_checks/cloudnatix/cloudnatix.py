from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.cloudnatix.config_models import ConfigMixin

from .metrics import METRIC_MAP


class CloudNatixCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = 'cloudnatix'

    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {
            "metrics": [METRIC_MAP],
        }
