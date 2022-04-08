TIDB_METRICS = [
    # query metrics
    'tidb_executor_statement_total',
    'tidb_server_execute_error_total',
    'tidb_server_handle_query_duration_seconds',
    'tidb_server_connections',
    # cpu metrics
    'process_cpu_seconds_total',
    # memory metrics
    'process_resident_memory_bytes',
    # no disk metrics for TiDB
    # no disk traffic metrics for TiDB
]
TIKV_METRICS = [
    # cpu metrics
    'process_cpu_seconds_total',
    # memory metrics
    'process_resident_memory_bytes',
    # disk metrics
    'tikv_engine_size_bytes',
    'tikv_store_size_bytes',
    # disk traffic metrics
    'tikv_io_bytes',
]
TIFLASH_METRICS = [
    # cpu metrics
    {'tiflash_proxy_process_cpu_seconds_total': 'process_cpu_seconds_total'},
    # memory metrics
    {'tiflash_proxy_process_resident_memory_bytes': 'process_resident_memory_bytes'},
    # disk metrics
    {'tiflash_system_current_metric_StoreSizeUsed': 'tiflash_store_size_used_bytes'},
    {'tiflash_system_current_metric_StoreSizeCapacity': 'tiflash_store_size_capacity_bytes'},
    # no disk traffic metrics for TiFlash
]
