
from typing import Any  # noqa: F401

from datadog_checks.base import OpenMetricsBaseCheckV2  # noqa: F401

from .config_models import ConfigMixin
from .metrics import METRIC_MAP


class RobustIntelligenceAiFirewallCheck(OpenMetricsBaseCheckV2, ConfigMixin):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'robust_intelligence_ai_firewall'

    def __init__(self, name, init_config, instances):
        super(RobustIntelligenceAiFirewallCheck, self).__init__(name, init_config, instances)

        self.openmetrics_endpoint = self.instance.get('openmetrics_endpoint')

    def get_default_config(self):
        default_config = {
            'openmetrics_endpoint': self.openmetrics_endpoint,
            'metrics': METRIC_MAP
        }

        return default_config
