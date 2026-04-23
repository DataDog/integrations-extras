EXPECTED_TIDB = {
    'metrics': {
        'tidb_cluster.tidb_executor_statement_total': [
            'type:Use',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_execute_error_total': [
            'type:schema:1146',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_handle_query_duration_seconds.sum': [
            'sql_type:Begin',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_connections': [
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_query_total': [
            'type:OK',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_disconnection_total': [
            'result:ok',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_plan_cache_total': [
            'type:hit',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_plan_cache_miss_total': [
            'type:miss',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_session_parse_duration_seconds.sum': [
            'sql_type:general',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_session_compile_duration_seconds.sum': [
            'sql_type:general',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_session_execute_duration_seconds.sum': [
            'type:general',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_session_transaction_duration_seconds.sum': [
            'sql_type:general',
            'type:commit',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_get_token_duration_seconds.sum': [
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_server_conn_idle_duration_seconds.sum': [
            'in_txn:0',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tidb_tikvclient_request_seconds.sum': [
            'store:1',
            'type:Prewrite',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.process_cpu_seconds_total': [
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.process_resident_memory_bytes': [
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:10080/metrics',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
    },
}

EXPECTED_TIFLASH = {
    'metrics': {
        'tidb_cluster.tiflash_store_size_used_bytes': [
            'tidb_cluster_component:tiflash',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tiflash_store_size_capacity_bytes': [
            'tidb_cluster_component:tiflash',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tiflash_syncing_data_freshness.sum': [
            'tidb_cluster_component:tiflash',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tiflash_syncing_data_freshness.count': [
            'tidb_cluster_component:tiflash',
            'tidb_cluster_name:test',
        ],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:8234/metrics',
            'tidb_cluster_component:tiflash',
            'tidb_cluster_name:test',
        ],
    },
}

EXPECTED_TIFLASH_PROXY = {
    'metrics': {
        'tidb_cluster.process_cpu_seconds_total': [
            'tidb_cluster_component:tiflash_proxy',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.process_resident_memory_bytes': [
            'tidb_cluster_component:tiflash_proxy',
            'tidb_cluster_name:test',
        ],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:20292/metrics',
            'tidb_cluster_component:tiflash_proxy',
            'tidb_cluster_name:test',
        ],
    },
}

EXPECTED_TIKV = {
    'metrics': {
        'tidb_cluster.tikv_engine_size_bytes': [
            'db:kv',
            'type:default',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_store_size_bytes': [
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
            'type:available',
        ],
        'tidb_cluster.tikv_io_bytes': [
            'op:read',
            'type:compaction',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_engine_flow_bytes': [
            'db:kv',
            'type:keys_read',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_thread_cpu_seconds_total': [
            'name:raftstore',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_grpc_msg_duration_seconds.sum': [
            'type:kv_get',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_raftstore_append_log_duration_seconds.sum': [
            'type:normal',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_raftstore_apply_log_duration_seconds.sum': [
            'type:normal',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_raftstore_commit_log_duration_seconds.sum': [
            'type:normal',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_raftstore_store_duration_secs.sum': [
            'type:normal',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_raftstore_apply_duration_secs.sum': [
            'type:normal',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.tikv_storage_engine_async_request_duration_seconds.sum': [
            'type:write',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.process_cpu_seconds_total': [
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.process_resident_memory_bytes': [
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:20180/metrics',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
    },
}

EXPECTED_PD = {
    'metrics': {
        'tidb_cluster.pd_client_cmd_handle_cmds_duration_seconds.sum': [
            'type:tso',
            'tidb_cluster_component:pd',
            'tidb_cluster_name:test',
        ],
        'tidb_cluster.pd_client_request_handle_requests_duration_seconds.sum': [
            'type:tso',
            'tidb_cluster_component:pd',
            'tidb_cluster_name:test',
        ],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:2379/metrics',
            'tidb_cluster_component:pd',
            'tidb_cluster_name:test',
        ],
    },
}
