from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

from .art_metrics import ART_METRIC_MAP
from .xray_metrics import XRAY_METRIC_MAP


class JfrogMetricsCheck(OpenMetricsBaseCheck):
    """
    Collect metrics from JFrog
    """

    def __init__(self, name, init_config, instancetype, instances=None):

        if instancetype == 'art':
            instance = instances[0]
            endpoint = instance.get('prometheus_url')
            if endpoint is None:
                raise ConfigurationError("Unable to find prometheus_url in config file.")

            instance.update(
                {
                    'prometheus_url': endpoint,
                    'namespace': 'jfrog.artifactory',
                    'metrics': [ART_METRIC_MAP],
                    'send_distribution_counts_as_monotonic': instance.get(
                        'send_distribution_counts_as_monotonic', True
                    ),
                    'send_distribution_sums_as_monotonic': instance.get('send_distribution_sums_as_monotonic', True),
                }
            )

        if instancetype == 'xray':
            instance = instances[0]
            endpoint = instance.get('prometheus_url')
            if endpoint is None:
                raise ConfigurationError("Unable to find prometheus_url in config file.")

            instance.update(
                {
                    'prometheus_url': endpoint,
                    'namespace': 'jfrog.xray',
                    'metrics': [XRAY_METRIC_MAP],
                    'send_distribution_counts_as_monotonic': instance.get(
                        'send_distribution_counts_as_monotonic', True
                    ),
                    'send_distribution_sums_as_monotonic': instance.get('send_distribution_sums_as_monotonic', True),
                }
            )

        super(JfrogMetricsCheck, self).__init__(name, init_config, [instance])
