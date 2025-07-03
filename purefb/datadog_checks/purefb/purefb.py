from datadog_checks.base import OpenMetricsBaseCheckV2

from .config_models import ConfigMixin
from .metrics import METRIC_MAP


class PureFBCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = "purefb"

    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(PureFBCheck, self).__init__(name, init_config, instances)
        self.openmetrics_endpoint = self.instance.get('openmetrics_endpoint')

    def get_default_config(self):
        default_config = {
            'openmetrics_endpoint': self.openmetrics_endpoint,
            'metrics': METRIC_MAP,
        }

        return default_config
