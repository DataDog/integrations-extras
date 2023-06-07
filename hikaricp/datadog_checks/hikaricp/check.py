from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.hikaricp.config_models import ConfigMixin
from datadog_checks.hikaricp.metrics import METRIC_MAP


class HikaricpCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = "hikaricp"

    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {"metrics": [METRIC_MAP]}
