TIDB_METRICS = [
    'tidb_executor_statement_total',
    'tidb_server_execute_error_total',
    'tidb_server_handle_query_duration_seconds',
    'tidb_server_connections',
    'process_cpu_seconds_total',
]
TIKV_METRICS = [
    'tikv_engine_size_bytes',
    'tikv_store_size_bytes',
    'tikv_thread_cpu_seconds_total',
    'tikv_io_bytes',
]
TIFLASH_METRICS = [
    {'tiflash_system_current_metric_StoreSizeUsed': 'tiflash_store_size_used_bytes'},
    {'tiflash_system_current_metric_StoreSizeCapacity': 'tiflash_store_size_capacity_bytes'},
    {"tiflash_proxy_process_cpu_seconds_total": "tiflash_cpu_seconds_total"},
]
