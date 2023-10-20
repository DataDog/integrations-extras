from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import MARIADB_SKYSQL_METRICS


class MariadbSkysqlCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = "skysql"
    OPEN_METRICS_ENDPOINT = "https://api.mariadb.com/observability/v2/metrics"

    def __init__(self, name, init_config, instances):
        super(MariadbSkysqlCheck, self).__init__(name, init_config, instances)
        self.check_initializations.appendleft(self._parse_config)

    def _parse_config(self):
        self.scraper_configs = []
        metrics_endpoint = self.instance.get('metrics_endpoint')

        config = {
            'openmetrics_endpoint': metrics_endpoint,
            'metrics': [MARIADB_SKYSQL_METRICS],
            'send_monotonic_counter': 'true',
        }

        config.update(self.instance)
        self.scraper_configs.append(config)

    def get_default_config(self):
        default_config = {
            'openmetrics_endpoint': self.OPEN_METRICS_ENDPOINT,
            'metrics': [MARIADB_SKYSQL_METRICS],
            'send_monotonic_counter': 'true',
        }
        return default_config
