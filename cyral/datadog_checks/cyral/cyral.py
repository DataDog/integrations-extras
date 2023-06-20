from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheck, is_affirmative

EVENT_TYPE = SOURCE_TYPE_NAME = 'cyral'


class CyralCheck(OpenMetricsBaseCheck):
    """
    Collect metrics from Cyral
    """

    DEFAULT_METRIC_LIMIT = 0

    def __init__(self, name, init_config, instances=None):
        instance = instances[0]
        endpoint = instance.get('prometheus_url')
        if endpoint is None:
            raise ConfigurationError("Unable to find prometheus_url in config file.")
        send_buckets = is_affirmative(instance.get('send_histograms_buckets', True))

        self.NAMESPACE = 'cyral'
        self.metrics_mapper = {
            'cyral_analysis_time': 'analysis_time',
            'cyral_analysis_time_counter': 'analysis_time_counter',
            'cyral_authentication_failure_count': 'authentication_failure_count',
            'cyral_catalog_query_count': 'catalog_query_count',
            'cyral_closed_client_conns_count': 'closed_client_conns_count',
            'cyral_closed_listeners_count': 'closed_listeners_count',
            'cyral_high_latency_query_count': 'high_latency_query_count',
            'cyral_open_client_conns_count': 'open_client_conns_count',
            'cyral_open_listeners_count': 'open_listeners_count',
            'cyral_policy_eval_time': 'policy_eval_time',
            'cyral_policy_eval_time_counter': 'policy_eval_time_counter',
            'cyral_policy_violation_count': 'policy_violation_count',
            'cyral_portscan_count': 'portscan_count',
            'cyral_queries_with_errors': 'queries_with_errors',
            'cyral_query_duration_count': 'query_duration_count',
            'cyral_query_duration_sum': 'query_duration_sum',
            'cyral_repo_dial_errors_count': 'repo_dial_errors_count',
            'cyral_row_count': 'row_count',
            'cyral_sql_parse_time': 'sql_parse_time',
            'cyral_sql_parse_time_counter': 'sql_parse_time_counter',
            'cyral_storage_watch_events_count': 'storage_watch_events_count',
            'cyral_wire_dial_errors_count': 'wire_dial_errors_count',
            'cyral_wire_parse_duration': 'wire_parse_duration',
            'cyral_wire_parse_duration_increments': 'wire_parse_duration_increments',
        }

        instance.update(
            {
                'prometheus_url': endpoint,
                'namespace': self.NAMESPACE,
                'metrics': [self.metrics_mapper],
                'send_histograms_buckets': send_buckets,
                'send_distribution_counts_as_monotonic': instance.get('send_distribution_counts_as_monotonic', True)
                # default to True to submit _count histogram/summary as monotonic
                # counts to Datadog
            }
        )

        super(CyralCheck, self).__init__(name, init_config, [instance])
