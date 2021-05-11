from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck


class JfrogPlatformCheck(OpenMetricsBaseCheck):
    """
    Collect metrics from JFrog
    """

    def __init__(self, name, init_config, instances=None):

        instance = instances[0]
        instancetype = instance.get('instance_type')
        endpoint = instance.get('prometheus_url')
        if endpoint is None:
            raise ConfigurationError("Unable to find prometheus_url in config file.")
        if instancetype == 'artifactory':

            instance.update(
                {
                    'prometheus_url': endpoint,
                    'namespace': 'jfrog.artifactory',
                    'metrics': ['sys*', 'jfrt*', 'app*'],
                    'send_distribution_counts_as_monotonic': instance.get(
                        'send_distribution_counts_as_monotonic', True
                    ),
                    'send_distribution_sums_as_monotonic': instance.get('send_distribution_sums_as_monotonic', True),
                }
            )

        elif instancetype == 'xray':

            instance.update(
                {
                    'prometheus_url': endpoint,
                    'namespace': 'jfrog.xray',
                    'metrics': ['app*', 'db*', 'go*', 'queue*', 'sys*', 'jfxr*'],
                    'send_distribution_counts_as_monotonic': instance.get(
                        'send_distribution_counts_as_monotonic', True
                    ),
                    'send_distribution_sums_as_monotonic': instance.get('send_distribution_sums_as_monotonic', True),
                }
            )
        else:
            raise ConfigurationError("Unable to recognize instance_type.")

        super(JfrogPlatformCheck, self).__init__(name, init_config, [instance])
