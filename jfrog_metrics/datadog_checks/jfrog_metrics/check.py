from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'jfrog_artifactory'


class JfrogMetricsCheck(OpenMetricsBaseCheck):
    """
    Collect metrics from JFrog
    """

    def __init__(self, name, init_config, instances=None):
        instance = instances[0]
        endpoint = instance.get('prometheus_url')
        if endpoint is None:
            raise ConfigurationError("Unable to find prometheus_url in config file.")

        self.NAMESPACE = 'jfrog_artifactory'
        self.metrics_mapper = {
            'app_disk_free_bytes': 'app_disk_free_bytes',
            'app_disk_total_bytes': 'app_disk_total_bytes',
            'sys_memory_free_bytes': 'sys_memory_free_bytes',
            'sys_memory_used_bytes': 'sys_memory_used_bytes',
            'jfrt_runtime_heap_processors_total': 'jfrt_runtime_heap_processors_total',
            'jfrt_db_connections_active_total': 'jfrt_db_connections_active_total',
        }

        instance.update(
            {
                'prometheus_url': endpoint,
                'namespace': self.NAMESPACE,
                'metrics': [self.metrics_mapper],
                'send_distribution_counts_as_monotonic': instance.get('send_distribution_counts_as_monotonic', True),
                'send_distribution_sums_as_monotonic': instance.get('send_distribution_sums_as_monotonic', True),
            }
        )

        super(JfrogMetricsCheck, self).__init__(name, init_config, [instance])
