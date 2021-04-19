from datadog_checks.base.stubs import aggregator

EXPECTED_TIDB_METRICS = {
    'tidb.pd_client_request_handle_requests_duration_seconds': aggregator.HISTOGRAM,
    'tidb.pd_client_cmd_handle_cmds_duration_seconds': aggregator.HISTOGRAM,
    'tidb.domain_load_schema_duration_seconds': aggregator.HISTOGRAM,
    'tidb.executor_statement_total': aggregator.COUNTER,
    'tidb.server_query_total': aggregator.COUNTER,
    'tidb.server_execute_error_total': aggregator.COUNTER,
    'tidb.server_connections': aggregator.GAUGE,
    'tidb.tikv_client_region_err_total': aggregator.COUNTER,
    'tidb.tikv_client_lock_resolver_actions_total': aggregator.COUNTER,
    'tidb.server_handle_query_duration_seconds': aggregator.HISTOGRAM,
    'tidb.session_transaction_duration_seconds': aggregator.HISTOGRAM,
    'tidb.tikv_client_txn_cmd_duration_seconds': aggregator.HISTOGRAM,
    'tidb.tikv_client_backoff_seconds': aggregator.HISTOGRAM,
}

EXPECTED_PD_METRICS = {
    'pd.tso_events': aggregator.GAUGE,
    'pd.cluster_status': aggregator.GAUGE,
    'pd.grpc_server_handling_seconds': aggregator.HISTOGRAM,
    'pd.regions_status': aggregator.GAUGE,
    'pd.hotspot_status': aggregator.GAUGE,
    'pd.scheduler_region_heartbeat': aggregator.GAUGE,
    'pd.scheduler_region_heartbeat_latency_seconds': aggregator.HISTOGRAM,
}

EXPECTED_TIKV_METRICS = {
    'tikv.raft_store_region_count': aggregator.COUNTER,
    'tikv.thread_cpu_seconds_total': aggregator.COUNTER,
    'tikv.engine_size_bytes': aggregator.COUNTER,
    'tikv.channel_full_total': aggregator.COUNTER,
    'tikv.server_report_failure_msg_total': aggregator.COUNTER,
    'tikv.scheduler_context_total': aggregator.COUNTER,
    'tikv.coprocessor_executor_count': aggregator.COUNTER,
    'tikv.coprocessor_request_duration_seconds': aggregator.COUNTER,
}

EXPECTED_CHECKS = {
    'tidb.prometheus.health',
}
