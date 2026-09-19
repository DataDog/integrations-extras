from datadog_checks.base import OpenMetricsBaseCheckV2

from .metrics import METRIC_MAP


class AmazonVpcCniCheck(OpenMetricsBaseCheckV2):
    __NAMESPACE__ = 'amazon_vpc_cni'
    DEFAULT_METRIC_LIMIT = 0

    def get_default_config(self):
        return {
            'metrics': [METRIC_MAP],
        }
