from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class WayfinderCheck(OpenMetricsBaseCheckV2):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'wayfinder'

    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(WayfinderCheck, self).__init__(name, init_config, instances)

        # Use self.instance to read the check configuration
        endpoint = self.instance.get('openmetrics_endpoint')
        if endpoint is None:
            raise ConfigurationError(
                "Configuration error. Missing URL for openmetrics_endpoint endpoint in config file."
            )

    def get_default_config(self):
        return {"metrics": [METRIC_MAP]}
