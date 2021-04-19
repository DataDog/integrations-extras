EXPECTED_TIDB_METRICS = {
    'tidb.executor_statement_total',
    'tidb.server_query_total',
    'tidb.server_execute_error_total',
    'tidb.server_connections',
    'tidb.tikv_client_region_err_total',
    'tidb.tikv_client_lock_resolver_actions_total',
    'tidb.server_handle_query_duration_seconds.count',
    'tidb.server_handle_query_duration_seconds.sum',
    'tidb.session_transaction_duration_seconds.count',
    'tidb.session_transaction_duration_seconds.sum',
    'tidb.tikv_client_txn_cmd_duration_seconds.count',
    'tidb.tikv_client_txn_cmd_duration_seconds.sum',
    'tidb.tikv_client_backoff_seconds.count',
    'tidb.tikv_client_backoff_seconds.sum',
    'tidb.pd_client_request_handle_requests_duration_seconds.count',
    'tidb.pd_client_request_handle_requests_duration_seconds.sum',
    'tidb.pd_client_cmd_handle_cmds_duration_seconds.count',
    'tidb.pd_client_cmd_handle_cmds_duration_seconds.sum',
    'tidb.domain_load_schema_duration_seconds.count',
    'tidb.domain_load_schema_duration_seconds.sum',
    'tidb.go_memstats_heap_inuse_bytes',
    'tidb.process_resident_memory_bytes',
}

EXPECTED_PD_METRICS = {
    'pd.tso_events',
    'pd.cluster_status',
    'pd.regions_status',
    'pd.hotspot_status',
    'pd.scheduler_region_heartbeat',
    'pd.grpc_server_handling_seconds.sum',
    'pd.grpc_server_handling_seconds.count',
    'pd.scheduler_region_heartbeat_latency_seconds.sum',
    'pd.scheduler_region_heartbeat_latency_seconds.count',
}

EXPECTED_TIKV_METRICS = {
    'tikv.raft_store_region_count',
    'tikv.thread_cpu_seconds_total',
    'tikv.engine_size_bytes',
    'tikv.channel_full_total',
    'tikv.server_report_failure_msg_total',
    'tikv.scheduler_context_total',
    'tikv.coprocessor_executor_count',
    'tikv.coprocessor_request_duration_seconds.sum',
    'tikv.coprocessor_request_duration_seconds.count',
}

EXPECTED_CHECKS = {
    'tidb.prometheus.health',
}
