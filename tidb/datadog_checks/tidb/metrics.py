TIDB_METRICS = {
    'pd_client_request_handle_requests_duration_seconds': 'tidb.pd_client_request_handle_requests_duration_seconds',
    'pd_client_cmd_handle_cmds_duration_seconds': 'tidb.pd_client_cmd_handle_cmds_duration_seconds',
    'tidb_domain_load_schema_duration_seconds': 'tidb.domain_load_schema_duration_seconds',
    'tidb_executor_statement_total': 'tidb.executor_statement_total',
    'tidb_server_query_total': 'tidb.server_query_total',
    'tidb_server_execute_error_total': 'tidb.server_execute_error_total',
    'tidb_server_connections': 'tidb.server_connections',
    'tidb_tikvclient_region_err_total': 'tidb.tikv_client_region_err_total',
    'tidb_tikvclient_lock_resolver_actions_total': 'tidb.tikv_client_lock_resolver_actions_total',
    'tidb_server_handle_query_duration_seconds': 'tidb.server_handle_query_duration_seconds',
    'tidb_session_transaction_duration_seconds': 'tidb.session_transaction_duration_seconds',
    'tidb_tikvclient_txn_cmd_duration_seconds': 'tidb.tikv_client_txn_cmd_duration_seconds',
    'tidb_tikvclient_backoff_seconds': 'tidb.tikv_client_backoff_seconds',
}

PD_METRICS = {
    'pd_tso_events': 'pd.tso_events',
    'pd_cluster_status': 'pd.cluster_status',
    'grpc_server_handling_seconds': 'pd.grpc_server_handling_seconds',
    'pd_regions_status': 'pd.regions_status',
    'pd_hotspot_status': 'pd.hotspot_status',
    'pd_scheduler_region_heartbeat': 'pd.scheduler_region_heartbeat',
    'pd_scheduler_region_heartbeat_latency_seconds': 'pd.scheduler_region_heartbeat',
}

TIKV_METRICS = {
    'tikv_raftstore_region_count': 'tikv.raft_store_region_count',
    'tikv_thread_cpu_seconds_total': 'tikv.thread_cpu_seconds_total',
    'tikv_engine_size_bytes': 'tikv.engine_size_bytes',
    'tikv_channel_full_total': 'tikv.channel_full_total',
    'tikv_server_report_failure_msg_total': 'tikv.server_report_failure_msg_total',
    'tikv_scheduler_contex_total': 'tikv.scheduler_context_total',
    'tikv_scheduler_context_total': 'tikv.scheduler_context_total',
    'tikv_coprocessor_executor_count': 'tikv.coprocessor_executor_count',
    'tikv_coprocessor_request_duration_seconds': 'tikv.coprocessor_request_duration_seconds',
}

GO_RUNTIME_METRICS = {
    'process_resident_memory_bytes': 'process_resident_memory_bytes',
    'go_memstats_heap_inuse_bytes': 'go_memstats_heap_inuse_bytes',
}
