METRIC_MAP = {
    ## API
    'api_call': 'request.duration',
    ## Token usage
    'localai_tokens': 'tokens',
    'localai_billed_requests': 'billed_requests',
    'localai_usage_unrecorded': 'usage_unrecorded',
    ## Model failover
    'localai_failover_switches': 'failover.switches',
    'localai_failover_target_up': 'failover.target_up',
    ## Context compression
    'localai_compression_events': 'compression.events',
    'localai_compression_ratio': 'compression.ratio',
    'localai_compression_duration_seconds': 'compression.duration',
}

RENAME_LABELS_MAP = {
    'endpoint': 'api_endpoint',
}

EXCLUDE_LABELS = [
    'otel_scope_name',
    'otel_scope_schema_url',
    'otel_scope_version',
]
