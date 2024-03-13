from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.emqx.config_models import ConfigMixin
from datadog_checks.emqx.metrics import METRIC_MAP


class EmqxCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = "emqx"

    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {"metrics": [METRIC_MAP]}
