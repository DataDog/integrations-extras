from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class ScaleopsCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'scaleops'
    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances):
        super(ScaleopsCheck, self).__init__(name, init_config, instances)

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
            'tag_by_endpoint': 'false',
            'exclude_labels': [
                'scaleops_id',
                'token',
                'version',
                'clusterId',
                'token_status',
                'customerName',
            ],
            'send_distribution_sums_as_monotonic': 'true',
            'send_distribution_counts_as_monotonic': 'true',
        }

    def check(self, _):
        super().check(_)
