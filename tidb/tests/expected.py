EXPECTED_TIDB_METRICS = {
    'tidb_cluster.tidb.executor_statement_total',
    'tidb_cluster.tidb.server_query_total',
    'tidb_cluster.tidb.server_execute_error_total',
    'tidb_cluster.tidb.server_connections',
    'tidb_cluster.tidb.tikv_client_region_err_total',
    'tidb_cluster.tidb.tikv_client_lock_resolver_actions_total',
    'tidb_cluster.tidb.server_handle_query_duration_seconds.count',
    'tidb_cluster.tidb.server_handle_query_duration_seconds.sum',
    'tidb_cluster.tidb.session_transaction_duration_seconds.count',
    'tidb_cluster.tidb.session_transaction_duration_seconds.sum',
    'tidb_cluster.tidb.tikv_client_txn_cmd_duration_seconds.count',
    'tidb_cluster.tidb.tikv_client_txn_cmd_duration_seconds.sum',
    'tidb_cluster.tidb.tikv_client_backoff_seconds.count',
    'tidb_cluster.tidb.tikv_client_backoff_seconds.sum',
    'tidb_cluster.tidb.pd_client_request_handle_requests_duration_seconds.count',
    'tidb_cluster.tidb.pd_client_request_handle_requests_duration_seconds.sum',
    'tidb_cluster.tidb.pd_client_cmd_handle_cmds_duration_seconds.count',
    'tidb_cluster.tidb.pd_client_cmd_handle_cmds_duration_seconds.sum',
    'tidb_cluster.tidb.domain_load_schema_duration_seconds.count',
    'tidb_cluster.tidb.domain_load_schema_duration_seconds.sum',
    'tidb_cluster.tidb.go_memstats_heap_inuse_bytes',
    'tidb_cluster.tidb.process_resident_memory_bytes',
}

EXPECTED_PD_METRICS = {
    'tidb_cluster.pd.tso_events',
    'tidb_cluster.pd.cluster_status',
    'tidb_cluster.pd.regions_status',
    'tidb_cluster.pd.hotspot_status',
    'tidb_cluster.pd.scheduler_region_heartbeat',
    'tidb_cluster.pd.grpc_server_handling_seconds.sum',
    'tidb_cluster.pd.grpc_server_handling_seconds.count',
    'tidb_cluster.pd.scheduler_region_heartbeat_latency_seconds.sum',
    'tidb_cluster.pd.scheduler_region_heartbeat_latency_seconds.count',
}

EXPECTED_TIKV_METRICS = {
    'tidb_cluster.tikv.raft_store_region_count',
    'tidb_cluster.tikv.thread_cpu_seconds_total',
    'tidb_cluster.tikv.engine_size_bytes',
    'tidb_cluster.tikv.channel_full_total',
    'tidb_cluster.tikv.server_report_failure_msg_total',
    'tidb_cluster.tikv.scheduler_context_total',
    'tidb_cluster.tikv.coprocessor_executor_count',
    'tidb_cluster.tikv.coprocessor_request_duration_seconds.sum',
    'tidb_cluster.tikv.coprocessor_request_duration_seconds.count',
}

EXPECTED_CHECKS = {
    'tidb_cluster.tidb.prometheus.health',
}
