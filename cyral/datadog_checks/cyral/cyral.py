from datadog_checks.base.checks.prometheus.prometheus_base import PrometheusCheck
from datadog_checks.base.errors import CheckException

EVENT_TYPE = SOURCE_TYPE_NAME = 'cyral'


class CyralCheck(PrometheusCheck):
    """
    Collect metrics from Cyral
    """

    def __init__(self, name, init_config, agentConfig, instances=None):
        super(CyralCheck, self).__init__(name, init_config, agentConfig, instances)
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

    def check(self, instance):
        endpoint = instance.get('prometheus_endpoint')
        if endpoint is None:
            raise CheckException("Unable to find prometheus_endpoint in config file.")

        send_buckets = instance.get('send_histograms_buckets', True)
        if send_buckets is not None and str(send_buckets).lower() == 'false':
            send_buckets = False
        else:
            send_buckets = True

        self.process(endpoint, send_histograms_buckets=send_buckets, instance=instance)
