"""
A SpiceDB metrics check for the Datadog agent.

Borrows heavily from the CockroachDB check in integrations-core.
"""

from datadog_checks.base.checks.openmetrics.v2 import OpenMetricsBaseCheckv2

from .config_models import ConfigMixin
from .metrics import METRICS_CONFIG


class SpicedbCheck(OpenMetricsBaseCheckv2, ConfigMixin):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'spicedb'

    def get_default_config(self):
        """
        Provides a default configuration, e.g. for tests.
        """
        return {
                'openmetrics_endpoint': 'http://localhost:9090/metrics',
                'metrics': METRICS_CONFIG
                }
