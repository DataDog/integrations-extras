EXPECTED_TIDB = {
    'metrics': {
        'tidb_cluster.tidb_executor_statement_total': [
            'type:Use',
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
        'tidb_cluster.process_cpu_seconds_total': [
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
        'tidb_cluster.tiflash_cpu_seconds_total': [
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
        # Since this metric has random value, we can't check it.
        'tidb_cluster.tikv_thread_cpu_seconds_total': None,
        'tidb_cluster.tikv_io_bytes': [
            'op:read',
            'type:compaction',
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
