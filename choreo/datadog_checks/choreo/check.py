from datadog_checks.base import OpenMetricsBaseCheckV2
from datadog_checks.choreo.config_models import ConfigMixin
from datadog_checks.choreo.metrics import METRICS_MAP


class ChoreoCheck(OpenMetricsBaseCheckV2, ConfigMixin):
    __NAMESPACE__ = 'choreo'

    def __init__(self, name, init_config, instances):
        super(ChoreoCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {'extra_headers': {'accept': "*/*"}, 'metrics': [METRICS_MAP]}
