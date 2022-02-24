from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.base import ConfigurationError
from .metrics import METRIC_MAP


class PureFACheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "purefa"

    def __init__(self, name, init_config, instances):
        super(PureFACheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)

    def get_default_config(self):
        return {'metrics': [METRIC_MAP]}

    def _parse_config(self):
        self.scraper_configs = []
        endpoint = self.instance.get('openmetrics_endpoint')

        if endpoint is None:
            raise ConfigurationError("Unable to find openmetrics URL in config file.")
