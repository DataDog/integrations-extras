# enterprise v2 metrics use the namespace 'rdse2'

REDIS_NODE = {
    'namedprocess_namegroup_thread_cpu_seconds_total': {
        'name': 'namedprocess_namegroup_thread_cpu_seconds_total',
        'type': 'gauge',
    },
    'no_of_expires': 'no_of_expires',
    'node_available_memory': 'node_available_memory',
    'node_available_memory_no_overbooking': 'node_available_memory_no_overbooking',
    'node_avg_latency': 'node_avg_latency',
    'node_cert_expiration_seconds': {
        'name': 'node_cert_expiration_seconds',
        'type': 'gauge',
    },
    'node_conns': 'node_conns',
    'node_cpu_idle': 'node_cpu_idle',
    'node_cpu_idle_max': 'node_cpu_idle_max',
    'node_cpu_idle_median': 'node_cpu_idle_median',
    'node_cpu_idle_min': 'node_cpu_idle_min',
    'node_cpu_iowait': 'node_cpu_iowait',
    'node_cpu_iowait_max': 'node_cpu_iowait_max',
    'node_cpu_iowait_median': 'node_cpu_iowait_median',
    'node_cpu_iowait_min': 'node_cpu_iowait_min',
    'node_cpu_irqs': 'node_cpu_irqs',
    'node_cpu_irqs_max': 'node_cpu_irqs_max',
    'node_cpu_irqs_median': 'node_cpu_irqs_median',
    'node_cpu_irqs_min': 'node_cpu_irqs_min',
    'node_cpu_nice': 'node_cpu_nice',
    'node_cpu_nice_max': 'node_cpu_nice_max',
    'node_cpu_nice_median': 'node_cpu_nice_median',
    'node_cpu_nice_min': 'node_cpu_nice_min',
    'node_cpu_steal': 'node_cpu_steal',
    'node_cpu_steal_max': 'node_cpu_steal_max',
    'node_cpu_steal_median': 'node_cpu_steal_median',
    'node_cpu_steal_min': 'node_cpu_steal_min',
    'node_cpu_system': 'node_cpu_system',
    'node_cpu_system_max': 'node_cpu_system_max',
    'node_cpu_system_median': 'node_cpu_system_median',
    'node_cpu_system_min': 'node_cpu_system_min',
    'node_cpu_user': 'node_cpu_user',
    'node_cpu_user_max': 'node_cpu_user_max',
    'node_cpu_user_median': 'node_cpu_user_median',
    'node_cpu_user_min': 'node_cpu_user_min',
    'node_cur_aof_rewrites': 'node_cur_aof_rewrites',
    'node_egress_bytes': 'node_egress_bytes',
    'node_egress_bytes_max': 'node_egress_bytes_max',
    'node_egress_bytes_median': 'node_egress_bytes_median',
    'node_egress_bytes_min': 'node_egress_bytes_min',
    'node_ephemeral_storage_avail': 'node_ephemeral_storage_avail',
    'node_ephemeral_storage_free': 'node_ephemeral_storage_free',
    'node_free_memory': 'node_free_memory',
    'node_ingress_bytes': 'node_ingress_bytes',
    'node_ingress_bytes_max': 'node_ingress_bytes_max',
    'node_ingress_bytes_median': 'node_ingress_bytes_median',
    'node_ingress_bytes_min': 'node_ingress_bytes_min',
    'node_persistent_storage_avail': 'node_persistent_storage_avail',
    'node_persistent_storage_free': 'node_persistent_storage_free',
    'node_provisional_memory': 'node_provisional_memory',
    'node_provisional_memory_no_overbooking': 'node_provisional_memory_no_overbooking',
    'node_total_req': 'node_total_req',
    'node_up': {
        'name': 'node_up',
        'type': 'gauge',
    },
}

REDIS_BIGSTORE = {
    'node_bigstore_free': {'name': 'node_bigstore_free', 'type': 'gauge'},
    'node_bigstore_iops': {'name': 'node_bigstore_iops', 'type': 'gauge'},
    'node_bigstore_kv_ops': {'name': 'node_bigstore_kv_ops', 'type': 'gauge'},
    'node_bigstore_throughput': {'name': 'node_bigstore_throughput', 'type': 'gauge'},
}

REDIS_FLASH = {
    'node_available_flash': 'node_available_flash',
    'node_available_flash_no_overbooking': 'node_available_flash_no_overbooking',
    'node_provisional_flash': 'node_provisional_flash',
    'node_provisional_flash_no_overbooking': 'node_provisional_flash_no_overbooking',
}


####### v2 #########

REDIS_CLUSTER = {
    'generation': 'generation',
    'has_quorum': 'has_quorum',
    'is_primary': 'is_primary',
    'license_shards_limit': 'license_shards_limit',
    'total_live_nodes_count': 'total_live_nodes_count',
    'total_nodes_count': 'total_nodes_count',
    'db_config': 'db_config',
}

# db_config{cluster="c36456.us-east5-mz.gcp.cloud.rlrcp.com",db="12880118",db_port="15213",db_version="7.4",instance="internal.c36456.us-east5-mz.gcp.cloud.rlrcp.com:8070",job="redis"}

REDIS_DATABASE = {
    'endpoint_client_connection_expired': 'endpoint_client_connection_expired',
    'endpoint_client_connections': 'endpoint_client_connections',
    'endpoint_client_disconnections': 'endpoint_client_disconnections',
    'endpoint_client_establishment_failures': 'endpoint_client_establishment_failures',
    'endpoint_client_tracking_off_requests': 'endpoint_client_tracking_off_requests',
    'endpoint_client_tracking_on_requests': 'endpoint_client_tracking_on_requests',
    'endpoint_dedicated_sconn_connections': 'endpoint_dedicated_sconn_connections',
    'endpoint_dedicated_sconn_proxy_disconnections': 'endpoint_dedicated_sconn_proxy_disconnections',
    'endpoint_dedicated_sconn_shard_disconnections': 'endpoint_dedicated_sconn_shard_disconnections',
    'endpoint_disposed_commands_after_client_caching': 'endpoint_disposed_commands_after_client_caching',
    'endpoint_egress': 'endpoint_egress',
    'endpoint_egress_pending': 'endpoint_egress_pending',
    'endpoint_egress_pending_discarded': 'endpoint_egress_pending_discarded',
    'endpoint_ingress': 'endpoint_ingress',
    'endpoint_internal_client_connections': 'endpoint_internal_client_connections',
    'endpoint_internal_client_disconnections': 'endpoint_internal_client_disconnections',
    'endpoint_internal_proxy_disconnections': 'endpoint_internal_proxy_disconnections',
    'endpoint_other_requests': 'endpoint_other_requests',
    'endpoint_other_requests_latency_histogram': 'endpoint_other_requests_latency_histogram',
    'endpoint_other_responses': 'endpoint_other_responses',
    'endpoint_proxy_disconnections': 'endpoint_proxy_disconnections',
    'endpoint_read_requests': 'endpoint_read_requests',
    'endpoint_read_requests_latency_histogram': 'endpoint_read_requests_latency_histogram',
    'endpoint_read_responses': 'endpoint_read_responses',
    'endpoint_sconn_application_handshake_failure': 'endpoint_sconn_application_handshake_failure',
    'endpoint_sconn_establishment_failure': 'endpoint_sconn_establishment_failure',
    'endpoint_shared_sconn_connections': 'endpoint_shared_sconn_connections',
    'endpoint_shared_sconn_proxy_disconnections': 'endpoint_shared_sconn_proxy_disconnections',
    'endpoint_shared_sconn_shard_disconnections': 'endpoint_shared_sconn_shard_disconnections',
    'endpoint_write_requests': 'endpoint_write_requests',
    'endpoint_write_requests_latency_histogram': 'endpoint_write_requests_latency_histogram',
    'endpoint_write_responses': 'endpoint_write_responses',
}

REDIS_REPLICATION = {

}

REDIS_SHARD = {
    'redis_server_active_defrag_running': 'redis_server_active_defrag_running',
    'redis_server_allocator_active': 'redis_server_allocator_active',
    'redis_server_allocator_allocated': 'redis_server_allocator_allocated',
    'redis_server_allocator_resident': 'redis_server_allocator_resident',
    'redis_server_aof_last_cow_size': 'redis_server_aof_last_cow_size',
    'redis_server_aof_rewrite_in_progress': 'redis_server_aof_rewrite_in_progress',
    'redis_server_aof_rewrites': 'redis_server_aof_rewrites',
    'redis_server_aof_delayed_fsync': 'redis_server_aof_delayed_fsync',
    'redis_server_blocked_clients': 'redis_server_blocked_clients',
    'redis_server_connected_clients': 'redis_server_connected_clients',
    'redis_server_connected_slaves': 'redis_server_connected_slaves',
    'redis_server_db0_avg_ttl': 'redis_server_db0_avg_ttl',
    'redis_server_expired_keys': 'redis_server_expired_keys',
    'redis_server_db0_keys': 'redis_server_db0_keys',
    'redis_server_evicted_keys': 'redis_server_evicted_keys',
    'redis_server_expire_cycle_cpu_milliseconds': 'redis_server_expire_cycle_cpu_milliseconds',
    'redis_server_expired_keys': 'redis_server_expired_keys',
    'redis_server_forwarding_state': 'redis_server_forwarding_state',
    'redis_server_keys_trimmed': 'redis_server_keys_trimmed',
    'redis_server_keyspace_read_hits': 'redis_server_keyspace_read_hits',
    'redis_server_keyspace_read_misses': 'redis_server_keyspace_read_misses',
    'redis_server_keyspace_write_hits': 'redis_server_keyspace_write_hits',
    'redis_server_keyspace_write_misses': 'redis_server_keyspace_write_misses',
    'redis_server_master_link_status': 'redis_server_master_link_status',
    'redis_server_master_repl_offset': 'redis_server_master_repl_offset',
    'redis_server_master_sync_in_progress': 'redis_server_master_sync_in_progress',
    'redis_server_max_process_mem': 'redis_server_max_process_mem',
    'redis_server_maxmemory': 'redis_server_maxmemory',
    'redis_server_mem_aof_buffer': 'redis_server_mem_aof_buffer',
    'redis_server_mem_clients_normal': 'redis_server_mem_clients_normal',
    'redis_server_mem_clients_slaves': 'redis_server_mem_clients_slaves',
    'redis_server_mem_fragmentation_ratio': 'redis_server_mem_fragmentation_ratio',
    'redis_server_mem_not_counted_for_evict': 'redis_server_mem_not_counted_for_evict',
    'redis_server_mem_replication_backlog': 'redis_server_mem_replication_backlog',
    'redis_server_module_fork_in_progress': 'redis_server_module_fork_in_progress',
    'namedprocess_namegroup_cpu_seconds_total': 'namedprocess_namegroup_cpu_seconds_total',
    'namedprocess_namegroup_thread_cpu_seconds_total': 'namedprocess_namegroup_thread_cpu_seconds_total',
    'namedprocess_namegroup_open_filedesc': 'namedprocess_namegroup_open_filedesc',
    'namedprocess_namegroup_memory_bytes': 'namedprocess_namegroup_memory_bytes',
    'namedprocess_namegroup_oldest_start_time_seconds': 'namedprocess_namegroup_oldest_start_time_seconds',
    'redis_server_rdb_bgsave_in_progress': 'redis_server_rdb_bgsave_in_progress',
    'redis_server_rdb_last_cow_size': 'redis_server_rdb_last_cow_size',
    'redis_server_rdb_saves': 'redis_server_rdb_saves',
    'redis_server_repl_touch_bytes': 'redis_server_repl_touch_bytes',
    'redis_server_total_commands_processed': 'redis_server_total_commands_processed',
    'redis_server_total_connections_received': 'redis_server_total_connections_received',
    'redis_server_total_net_input_bytes': 'redis_server_total_net_input_bytes',
    'redis_server_total_net_output_bytes': 'redis_server_total_net_output_bytes',
    'redis_server_up': 'redis_server_up',
    'redis_server_used_memory': 'redis_server_used_memory',
}

REDIS_NODE = {
    'node_available_flash_bytes': 'node_available_flash_bytes',
    'node_available_flash_no_overbooking_bytes': 'node_available_flash_no_overbooking_bytes',
    'node_available_memory_bytes': 'node_available_memory_bytes',
    'node_available_memory_no_overbooking_bytes': 'node_available_memory_no_overbooking_bytes',
    'node_bigstore_free_bytes': 'node_bigstore_free_bytes',
    'node_cert_expires_in_seconds': 'node_cert_expires_in_seconds',
    'node_ephemeral_storage_avail_bytes': 'node_ephemeral_storage_avail_bytes',
    'node_ephemeral_storage_free_bytes': 'node_ephemeral_storage_free_bytes',
    'node_memory_MemFree_bytes': 'node_memory_MemFree_bytes',
    'node_persistent_storage_avail_bytes': 'node_persistent_storage_avail_bytes',
    'node_persistent_storage_free_bytes': 'node_persistent_storage_free_bytes',
    'node_provisional_flash_bytes': 'node_provisional_flash_bytes',
    'node_provisional_flash_no_overbooking_bytes': 'node_provisional_flash_no_overbooking_bytes',
    'node_provisional_memory_bytes': 'node_provisional_memory_bytes',
    'node_provisional_memory_no_overbooking_bytes': 'node_provisional_memory_no_overbooking_bytes',
    'node_metrics_up': 'node_metrics_up',
}

REDIS_LDAP = {
    'directory_cache_hits': 'directory_cache_hits',
    'directory_cache_miss_then_hits': 'directory_cache_miss_then_hits',
    'directory_cache_misses': 'directory_cache_misses',
    'directory_cache_refreshes': 'directory_cache_refreshes',
    'directory_cache_stales': 'directory_cache_stales',
    'directory_conn_connections': 'directory_conn_connections',
    'directory_conn_disconnections': 'directory_conn_disconnections',
    'directory_conn_failed_connections': 'directory_conn_failed_connections',
    'directory_queries_error': 'directory_queries_error',
    'directory_queries_expired': 'directory_queries_expired',
    'directory_queries_no_conn': 'directory_queries_no_conn',
    'directory_queries_sent': 'directory_queries_sent',
    'directory_queries_success': 'directory_queries_success',
    'directory_queries_wrongpass': 'directory_queries_wrongpass',
    'directory_requests': 'directory_requests',
}

REDIS_NETWORK = {
    'node_network_receive_bytes_total': 'node_network_receive_bytes_total',
    'node_network_receive_compressed_total': 'node_network_receive_compressed_total',
    'node_network_receive_drop_total': 'node_network_receive_drop_total',
    'node_network_receive_errs_total': 'node_network_receive_errs_total',
    'node_network_receive_fifo_total': 'node_network_receive_fifo_total',
    'node_network_receive_frame_total': 'node_network_receive_frame_total',
    'node_network_receive_multicast_total': 'node_network_receive_multicast_total',
    'node_network_receive_nohandler_total': 'node_network_receive_nohandler_total',
    'node_network_receive_packets_total': 'node_network_receive_packets_total',
    'node_network_transmit_bytes_total': 'node_network_transmit_bytes_total',
    'node_network_transmit_carrier_total': 'node_network_transmit_carrier_total',
    'node_network_transmit_colls_total': 'node_network_transmit_colls_total',
    'node_network_transmit_compressed_total': 'node_network_transmit_compressed_total',
    'node_network_transmit_drop_total': 'node_network_transmit_drop_total',
    'node_network_transmit_errs_total': 'node_network_transmit_errs_total',
    'node_network_transmit_fifo_total': 'node_network_transmit_fifo_total',
    'node_network_transmit_packets_total': 'node_network_transmit_packets_total',
}

REDIS_MEMORY = {}

REDIS_X509 = {
    'x509_cert_expired': 'x509_cert_expired',
    'x509_cert_expires_in_seconds': 'x509_cert_expires_in_seconds',
    'x509_cert_not_after': 'x509_cert_not_after',
    'x509_cert_not_before': 'x509_cert_not_before',
    'x509_cert_valid_since_seconds': 'x509_cert_valid_since_seconds',
    'x509_exporter_build_info': 'x509_exporter_build_info',
    'x509_read_errors': 'x509_read_errors',
}

REDIS_FILESYSTEM = {
    'node_filesystem_avail_bytes': 'node_filesystem_avail_bytes',
    'node_filesystem_device_error': 'node_filesystem_device_error',
    'node_filesystem_files': 'node_filesystem_files',
    'node_filesystem_files_free': 'node_filesystem_files_free',
    'node_filesystem_free_bytes': 'node_filesystem_free_bytes',
    'node_filesystem_readonly': 'node_filesystem_readonly',
    'node_filesystem_size_bytes': 'node_filesystem_size_bytes',
}

REDIS_DISK = {
    'node_disk_discard_time_seconds_total': 'node_disk_discard_time_seconds_total',
    'node_disk_discarded_sectors_total': 'node_disk_discarded_sectors_total',
    'node_disk_discards_completed_total': 'node_disk_discards_completed_total',
    'node_disk_discards_merged_total': 'node_disk_discards_merged_total',
    'node_disk_flush_requests_time_seconds_total': 'node_disk_flush_requests_time_seconds_total',
    'node_disk_flush_requests_total': 'node_disk_flush_requests_total',
    'node_disk_info': 'node_disk_info',
    'node_disk_io_now': 'node_disk_io_now',
    'node_disk_io_time_seconds_total': 'node_disk_io_time_seconds_total',
    'node_disk_io_time_weighted_seconds_total': 'node_disk_io_time_weighted_seconds_total',
    'node_disk_read_bytes_total': 'node_disk_read_bytes_total',
    'node_disk_read_time_seconds_total': 'node_disk_read_time_seconds_total',
    'node_disk_reads_completed_total': 'node_disk_reads_completed_total',
    'node_disk_reads_merged_total': 'node_disk_reads_merged_total',
    'node_disk_write_time_seconds_total': 'node_disk_write_time_seconds_total',
    'node_disk_writes_completed_total': 'node_disk_writes_completed_total',
    'node_disk_writes_merged_total': 'node_disk_writes_merged_total',
    'node_disk_written_bytes_total': 'node_disk_written_bytes_total',
}

REDIS_PROCESS = {
    'process_cpu_seconds_total': 'process_cpu_seconds_total',
    'process_exporter_build_info': 'process_exporter_build_info',
    'process_max_fds': 'process_max_fds',
    'process_open_fds': 'process_open_fds',
    'process_resident_memory_bytes': 'process_resident_memory_bytes',
    'process_start_time_seconds': 'process_start_time_seconds',
    'process_virtual_memory_bytes': 'process_virtual_memory_bytes',
    'process_virtual_memory_max_bytes': 'process_virtual_memory_max_bytes',
}

REDIS_PRESSURE = {
    'node_pressure_cpu_waiting_seconds_total': 'node_pressure_cpu_waiting_seconds_total',
    'node_pressure_io_stalled_seconds_total': 'node_pressure_io_stalled_seconds_total',
    'node_pressure_io_waiting_seconds_total': 'node_pressure_io_waiting_seconds_total',
    'node_pressure_memory_stalled_seconds_total': 'node_pressure_memory_stalled_seconds_total',
    'node_pressure_memory_waiting_seconds_total': 'node_pressure_memory_waiting_seconds_total',
}

REDIS_INFO = {
    'node_dmi_info': 'node_dmi_info',
    'node_os_info': 'node_os_info',
}

DEFAULT_METRICS = [
    REDIS_CLUSTER,
    REDIS_DATABASE,
    REDIS_NODE,
    REDIS_SHARD,
]

ADDITIONAL_METRICS = {
    'RDSE.REPLICATION': REDIS_REPLICATION,
    'RDSE.LDAP': REDIS_LDAP,
    'RDSE.NETWORK': REDIS_NETWORK,
    'RDSE.MEMORY': REDIS_MEMORY,
    'RDSE.X509': REDIS_X509,
    'RDSE.DISK': REDIS_DISK,
    'RDSE.FILESYSTEM': REDIS_FILESYSTEM,
    'RDSE.PROCESS': REDIS_PROCESS,
    'RDSE.PRESSURE': REDIS_PRESSURE,
    'RDSE.INFO': REDIS_INFO
}


# ADDITIONAL_METRICS = {
#     'RDSE.REPLICATION': REDIS_REPLICATION,
#     'RDSE.SHARDREPL': REDIS_SHARD_REPLICATION,
#     'RDSE.LISTENER': REDIS_LISTENER,
#     'RDSE.PROXY': REDIS_PROXY,
#     'RDSE.BIGSTORE': REDIS_BIGSTORE,
#     'RDSE.FLASH': REDIS_FLASH,
# }
