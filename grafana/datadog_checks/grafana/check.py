from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class GrafanaCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'grafana'
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(GrafanaCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {"metrics": [METRIC_MAP]}
