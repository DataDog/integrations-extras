from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.fluxcd.config_models import ConfigMixin
from datadog_checks.fluxcd.metrics import METRIC_MAP


class FluxcdCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = "fluxcd"

    def get_default_config(self):
        return {"metrics": [METRIC_MAP]}
