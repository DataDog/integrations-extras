TIDB_METRICS = [
    # query metrics
    'tidb_executor_statement_total',
    'tidb_server_execute_error_total',
    'tidb_server_handle_query_duration_seconds',
    'tidb_server_connections',
    'tidb_server_query_total',
    'tidb_server_disconnection_total',
    'tidb_server_plan_cache_total',
    'tidb_server_plan_cache_miss_total',
    # session phase duration metrics
    'tidb_session_parse_duration_seconds',
    'tidb_session_compile_duration_seconds',
    'tidb_session_execute_duration_seconds',
    'tidb_session_transaction_duration_seconds',
    'tidb_server_get_token_duration_seconds',
    'tidb_server_conn_idle_duration_seconds',
    # tikv client metrics from TiDB side
    'tidb_tikvclient_request_seconds',
    # cpu metrics
    'process_cpu_seconds_total',
    'process_start_time_seconds',
    # memory metrics
    'process_resident_memory_bytes',
    # no disk metrics for TiDB
    # no disk traffic metrics for TiDB
]
TIKV_METRICS = [
    # cpu metrics
    'process_cpu_seconds_total',
    'tikv_thread_cpu_seconds_total',
    # memory metrics
    'process_resident_memory_bytes',
    # disk metrics
    'tikv_engine_size_bytes',
    'tikv_store_size_bytes',
    # disk traffic metrics
    'tikv_io_bytes',
    'tikv_engine_flow_bytes',
    # gRPC metrics
    'tikv_grpc_msg_duration_seconds',
    # raftstore metrics
    'tikv_raftstore_append_log_duration_seconds',
    'tikv_raftstore_apply_log_duration_seconds',
    'tikv_raftstore_commit_log_duration_seconds',
    'tikv_raftstore_store_duration_secs',
    'tikv_raftstore_apply_duration_secs',
    'tikv_storage_engine_async_request_duration_seconds',
]
TIFLASH_METRICS = [
    # cpu metrics
    {'tiflash_proxy_process_cpu_seconds_total': 'process_cpu_seconds_total'},
    # memory metrics
    {'tiflash_proxy_process_resident_memory_bytes': 'process_resident_memory_bytes'},
    # disk metrics
    {'tiflash_system_current_metric_StoreSizeUsed': 'tiflash_store_size_used_bytes'},
    {'tiflash_system_current_metric_StoreSizeCapacity': 'tiflash_store_size_capacity_bytes'},
    # replication lag metrics
    {'tiflash_syncing_data_freshness': 'tiflash_syncing_data_freshness'},
]
PD_METRICS = [
    # client command duration metrics
    'pd_client_cmd_handle_cmds_duration_seconds',
    'pd_client_request_handle_requests_duration_seconds',
]
