from typing import Any  # noqa: F401

from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.caddy.config_models import ConfigMixin
from datadog_checks.caddy.metrics import METRIC_MAP


class CaddyCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = 'caddy'

    def get_default_config(self):
        return {
            "metrics": [METRIC_MAP],
        }
