# enterprise v2 metrics use the namespace 'rdse2'

# NB v2 metrics that include type declarations do so to point out those that need to be typed by the endpoint


# REDIS_BIGSTORE = {
#     'node_bigstore_free': {'name': 'node_bigstore_free', 'type': 'gauge'},
#     'node_bigstore_iops': {'name': 'node_bigstore_iops', 'type': 'gauge'},
#     'node_bigstore_kv_ops': {'name': 'node_bigstore_kv_ops', 'type': 'gauge'},
#     'node_bigstore_throughput': {'name': 'node_bigstore_throughput', 'type': 'gauge'},
# }
#
# REDIS_FLASH = {
#     'node_available_flash': 'node_available_flash',
#     'node_available_flash_no_overbooking': 'node_available_flash_no_overbooking',
#     'node_provisional_flash': 'node_provisional_flash',
#     'node_provisional_flash_no_overbooking': 'node_provisional_flash_no_overbooking',
# }


####### v2 #########

REDIS_CLUSTER = {
    'generation': 'generation',
    'has_quorum': 'has_quorum',
    'is_primary': 'is_primary',
    # 'license_shards_limit': 'license_shards_limit',
    'total_live_nodes_count': 'total_live_nodes_count',
    'total_nodes_count': 'total_nodes_count',
}

# db_config{cluster="c36456.us-east5-mz.gcp.cloud.rlrcp.com",db="12880118",db_port="15213",db_version="7.4",instance="internal.c36456.us-east5-mz.gcp.cloud.rlrcp.com:8070",job="redis"}

REDIS_DATABASE = {
    # 'db_config': 'db_config',
    'db_memory_limit_bytes': 'db_memory_limit_bytes',
    # 'db_status': 'db_status',
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
    'namedprocess_namegroup_cpu_seconds': 'namedprocess_namegroup_cpu_seconds',
    'namedprocess_namegroup_thread_cpu_seconds': 'namedprocess_namegroup_thread_cpu_seconds',
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
    'x509_cert_expires_in_seconds': 'x509_cert_expires_in_seconds',
    'x509_exporter_build_info': 'x509_exporter_build_info',
    'x509_read_errors': 'x509_read_errors',
    'x509_cert_valid_since_seconds': 'x509_cert_valid_since_seconds',
    'x509_cert_not_before': 'x509_cert_not_before',
    'x509_cert_not_after': 'x509_cert_not_after',
    'x509_cert_expired': 'x509_cert_expired',
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

REDIS_INFO = {
    'node_disk_info': 'node_disk_info',
    'node_dmi_info': 'node_dmi_info',
    'node_os_info': 'node_os_info',
}

### END DEFAULT

REDIS_REPLICATION = {
    'database_syncer_config': 'database_syncer_config',
    'database_syncer_current_status': 'database_syncer_current_status',
    'database_syncer_dst_connectivity_state': 'database_syncer_dst_connectivity_state',
    'database_syncer_dst_connectivity_state_ms': 'database_syncer_dst_connectivity_state_ms',
    'database_syncer_dst_lag': 'database_syncer_dst_lag',
    'database_syncer_dst_repl_offset': 'database_syncer_dst_repl_offset',
    'database_syncer_flush_counter': 'database_syncer_flush_counter',
    'database_syncer_ingress_bytes': 'database_syncer_ingress_bytes',
    'database_syncer_ingress_bytes_decompressed': 'database_syncer_ingress_bytes_decompressed',
    'database_syncer_internal_state': 'database_syncer_internal_state',
    'database_syncer_lag_ms': 'database_syncer_lag_ms',
    'database_syncer_rdb_size': 'database_syncer_rdb_size',
    'database_syncer_rdb_transferred': 'database_syncer_rdb_transferred',
    'database_syncer_src_connectivity_state': 'database_syncer_src_connectivity_state',
    'database_syncer_src_connectivity_state_ms': 'database_syncer_src_connectivity_state_ms',
    'database_syncer_src_repl_offset': 'database_syncer_src_repl_offset',
    'database_syncer_state': 'database_syncer_state',
    'database_syncer_syncer_repl_offset': 'database_syncer_syncer_repl_offset',
    'database_syncer_total_requests': 'database_syncer_total_requests',
    'database_syncer_total_responses': 'database_syncer_total_responses',
}

REDIS_SHARD_REPLICATION = {
    'redis_crdt_backlog_histlen': 'redis_crdt_backlog_histlen',
    'redis_crdt_backlog_idx': 'redis_crdt_backlog_idx',
    'redis_crdt_backlog_master_offset': 'redis_crdt_backlog_master_offset',
    'redis_crdt_backlog_offset': 'redis_crdt_backlog_offset',
    'redis_crdt_backlog_refs': 'redis_crdt_backlog_refs',
    'redis_crdt_backlog_size': 'redis_crdt_backlog_size',
    'redis_crdt_clock': 'redis_crdt_clock',
    'redis_crdt_effect_reqs': 'redis_crdt_effect_reqs',
    'redis_crdt_gc_attempted': 'redis_crdt_gc_attempted',
    'redis_crdt_gc_collected': 'redis_crdt_gc_collected',
    'redis_crdt_gc_elements_attempted': 'redis_crdt_gc_elements_attempted',
    'redis_crdt_gc_elements_collected': 'redis_crdt_gc_elements_collected',
    'redis_crdt_gc_pending': 'redis_crdt_gc_pending',
    'redis_crdt_gc_skipped': 'redis_crdt_gc_skipped',
    'redis_crdt_key_headers': 'redis_crdt_key_headers',
    'redis_crdt_list_trimmed_vertices': 'redis_crdt_list_trimmed_vertices',
    'redis_crdt_merge_reqs': 'redis_crdt_merge_reqs',
    'redis_crdt_oom_latch': 'redis_crdt_oom_latch',
    'redis_crdt_ovc_filtered_effect_reqs': 'redis_crdt_ovc_filtered_effect_reqs',
    'redis_crdt_peer_dst_id': 'redis_crdt_peer_dst_id',
    'redis_crdt_peer_id': 'redis_crdt_peer_id',
    'redis_crdt_peer_lag': 'redis_crdt_peer_lag',
    'redis_crdt_peer_offset': 'redis_crdt_peer_offset',
    'redis_crdt_peer_peer_state': 'redis_crdt_peer_peer_state',
    'redis_crdt_pending_list_trimmed_vertices': 'redis_crdt_pending_list_trimmed_vertices',
    'redis_crdt_raw_dbsize': 'redis_crdt_raw_dbsize',
    'redis_crdt_replica_config_version': 'redis_crdt_replica_config_version',
    'redis_crdt_replica_max_ops_lag': 'redis_crdt_replica_max_ops_lag',
    'redis_crdt_replica_min_ops_lag': 'redis_crdt_replica_min_ops_lag',
    'redis_crdt_replica_shards': 'redis_crdt_replica_shards',
    'redis_crdt_replica_slot_coverage_by_any_ovc': 'redis_crdt_replica_slot_coverage_by_any_ovc',
    'redis_crdt_replica_slot_coverage_by_only_ovc': 'redis_crdt_replica_slot_coverage_by_only_ovc',
    'redis_crdt_replica_slots': 'redis_crdt_replica_slots',
    'redis_crdt_stale_replica': 'redis_crdt_stale_replica',
    'redis_crdt_ts_key_headers': 'redis_crdt_ts_key_headers',
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
    'node_network_receive_bytes': 'node_network_receive_bytes',
    'node_network_receive_compressed': 'node_network_receive_compressed',
    'node_network_receive_drop': 'node_network_receive_drop',
    'node_network_receive_errs': 'node_network_receive_errs',
    'node_network_receive_fifo': 'node_network_receive_fifo',
    'node_network_receive_frame': 'node_network_receive_frame',
    'node_network_receive_multicast': 'node_network_receive_multicast',
    'node_network_receive_nohandler': 'node_network_receive_nohandler',
    'node_network_receive_packets': 'node_network_receive_packets',
    'node_network_transmit_bytes': 'node_network_transmit_bytes',
    'node_network_transmit_carrier': 'node_network_transmit_carrier',
    'node_network_transmit_colls': 'node_network_transmit_colls',
    'node_network_transmit_compressed': 'node_network_transmit_compressed',
    'node_network_transmit_drop': 'node_network_transmit_drop',
    'node_network_transmit_errs': 'node_network_transmit_errs',
    'node_network_transmit_fifo': 'node_network_transmit_fifo',
    'node_network_transmit_packets': 'node_network_transmit_packets',
}

REDIS_MEMORY = {
    'node_memory_Active_anon_bytes': 'node_memory_Active_anon_bytes',
    'node_memory_Active_bytes': 'node_memory_Active_bytes',
    'node_memory_Active_file_bytes': 'node_memory_Active_file_bytes',
    'node_memory_AnonHugePages_bytes': 'node_memory_AnonHugePages_bytes',
    'node_memory_AnonPages_bytes': 'node_memory_AnonPages_bytes',
    'node_memory_Bounce_bytes': 'node_memory_Bounce_bytes',
    'node_memory_Buffers_bytes': 'node_memory_Buffers_bytes',
    'node_memory_Cached_bytes': 'node_memory_Cached_bytes',
    'node_memory_CommitLimit_bytes': 'node_memory_CommitLimit_bytes',
    'node_memory_Committed_AS_bytes': 'node_memory_Committed_AS_bytes',
    'node_memory_DirectMap1G_bytes': 'node_memory_DirectMap1G_bytes',
    'node_memory_DirectMap2M_bytes': 'node_memory_DirectMap2M_bytes',
    'node_memory_DirectMap4k_bytes': 'node_memory_DirectMap4k_bytes',
    'node_memory_Dirty_bytes': 'node_memory_Dirty_bytes',
    'node_memory_FileHugePages_bytes': 'node_memory_FileHugePages_bytes',
    'node_memory_FilePmdMapped_bytes': 'node_memory_FilePmdMapped_bytes',
    'node_memory_HardwareCorrupted_bytes': 'node_memory_HardwareCorrupted_bytes',
    'node_memory_HugePages_Free': 'node_memory_HugePages_Free',
    'node_memory_HugePages_Rsvd': 'node_memory_HugePages_Rsvd',
    'node_memory_HugePages_Surp': 'node_memory_HugePages_Surp',
    'node_memory_HugePages_Total': 'node_memory_HugePages_Total',
    'node_memory_Hugepagesize_bytes': 'node_memory_Hugepagesize_bytes',
    'node_memory_Hugetlb_bytes': 'node_memory_Hugetlb_bytes',
    'node_memory_Inactive_anon_bytes': 'node_memory_Inactive_anon_bytes',
    'node_memory_Inactive_bytes': 'node_memory_Inactive_bytes',
    'node_memory_Inactive_file_bytes': 'node_memory_Inactive_file_bytes',
    'node_memory_KReclaimable_bytes': 'node_memory_KReclaimable_bytes',
    'node_memory_KernelStack_bytes': 'node_memory_KernelStack_bytes',
    'node_memory_Mapped_bytes': 'node_memory_Mapped_bytes',
    'node_memory_MemAvailable_bytes': 'node_memory_MemAvailable_bytes',
    'node_memory_MemFree_bytes': 'node_memory_MemFree_bytes',
    'node_memory_MemTotal_bytes': 'node_memory_MemTotal_bytes',
    'node_memory_Mlocked_bytes': 'node_memory_Mlocked_bytes',
    'node_memory_NFS_Unstable_bytes': 'node_memory_NFS_Unstable_bytes',
    'node_memory_PageTables_bytes': 'node_memory_PageTables_bytes',
    'node_memory_Percpu_bytes': 'node_memory_Percpu_bytes',
    'node_memory_SReclaimable_bytes': 'node_memory_SReclaimable_bytes',
    'node_memory_SUnreclaim_bytes': 'node_memory_SUnreclaim_bytes',
    'node_memory_ShmemHugePages_bytes': 'node_memory_ShmemHugePages_bytes',
    'node_memory_ShmemPmdMapped_bytes': 'node_memory_ShmemPmdMapped_bytes',
    'node_memory_Shmem_bytes': 'node_memory_Shmem_bytes',
    'node_memory_Slab_bytes': 'node_memory_Slab_bytes',
    'node_memory_SwapCached_bytes': 'node_memory_SwapCached_bytes',
    'node_memory_SwapFree_bytes': 'node_memory_SwapFree_bytes',
    'node_memory_SwapTotal_bytes': 'node_memory_SwapTotal_bytes',
    'node_memory_Unevictable_bytes': 'node_memory_Unevictable_bytes',
    'node_memory_VmallocChunk_bytes': 'node_memory_VmallocChunk_bytes',
    'node_memory_VmallocTotal_bytes': 'node_memory_VmallocTotal_bytes',
    'node_memory_VmallocUsed_bytes': 'node_memory_VmallocUsed_bytes',
    'node_memory_WritebackTmp_bytes': 'node_memory_WritebackTmp_bytes',
    'node_memory_Writeback_bytes': 'node_memory_Writeback_bytes',
}

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
    'node_disk_discard_time_seconds': 'node_disk_discard_time_seconds',
    'node_disk_discarded_sectors': 'node_disk_discarded_sectors',
    'node_disk_discards_completed': 'node_disk_discards_completed',
    'node_disk_discards_merged': 'node_disk_discards_merged',
    'node_disk_flush_requests_time_seconds': 'node_disk_flush_requests_time_seconds',
    'node_disk_flush_requests': 'node_disk_flush_requests',
    'node_disk_io_now': 'node_disk_io_now',
    'node_disk_io_time_seconds': 'node_disk_io_time_seconds',
    'node_disk_io_time_weighted_seconds': 'node_disk_io_time_weighted_seconds',
    'node_disk_read_bytes': 'node_disk_read_bytes',
    'node_disk_read_time_seconds': 'node_disk_read_time_seconds',
    'node_disk_reads_completed': 'node_disk_reads_completed',
    'node_disk_reads_merged': 'node_disk_reads_merged',
    'node_disk_write_time_seconds': 'node_disk_write_time_seconds',
    'node_disk_writes_completed': 'node_disk_writes_completed',
    'node_disk_writes_merged': 'node_disk_writes_merged',
    'node_disk_written_bytes': 'node_disk_written_bytes',
}

REDIS_PROCESS = {
    'node_processes_max_threads': 'node_processes_max_threads',
    'process_exporter_build_info': 'process_exporter_build_info',
    'node_processes_max_processes': 'node_processes_max_processes',
    'node_processes_pids': 'node_processes_pids',
    'node_processes_state': 'node_processes_state',
    'node_processes_threads': 'node_processes_threads',
    'node_processes_threads_state': 'node_processes_threads_state',
}

REDIS_PRESSURE = {
    'node_pressure_cpu_waiting_seconds': 'node_pressure_cpu_waiting_seconds',
    'node_pressure_io_stalled_seconds': 'node_pressure_io_stalled_seconds',
    'node_pressure_io_waiting_seconds': 'node_pressure_io_waiting_seconds',
    'node_pressure_memory_stalled_seconds': 'node_pressure_memory_stalled_seconds',
    'node_pressure_memory_waiting_seconds': 'node_pressure_memory_waiting_seconds',
}

REDIS_SEARCH = {
    'redis_server_search_number_of_indexes': 'redis_server_search_number_of_indexes',
    'redis_server_search_number_of_active_indexes': 'redis_server_search_number_of_active_indexes',
    'redis_server_search_number_of_active_indexes_running_queries': 'redis_server_search_number_of_active_indexes_running_queries',
    'redis_server_search_number_of_active_indexes_indexing': 'redis_server_search_number_of_active_indexes_indexing',
    'redis_server_search_total_active_write_threads': 'redis_server_search_total_active_write_threads',
    'redis_server_search_fields_text_Text': 'redis_server_search_fields_text_Text',
    'redis_server_search_fields_text_Sortable': 'redis_server_search_fields_text_Sortable',
    'redis_server_search_fields_text_NoIndex': 'redis_server_search_fields_text_NoIndex',
    'redis_server_search_fields_numeric_Numeric': 'redis_server_search_fields_numeric_Numeric',
    'redis_server_search_fields_numeric_Sortable': 'redis_server_search_fields_numeric_Sortable',
    'redis_server_search_fields_numeric_NoIndex': 'redis_server_search_fields_numeric_NoIndex',
    'redis_server_search_fields_tag_Tag': 'redis_server_search_fields_tag_Tag',
    'redis_server_search_fields_tag_Sortable': 'redis_server_search_fields_tag_Sortable',
    'redis_server_search_fields_tag_NoIndex': 'redis_server_search_fields_tag_NoIndex',
    'redis_server_search_fields_tag_CaseSensitive': 'redis_server_search_fields_tag_CaseSensitive',
    'redis_server_search_fields_geo_Geo': 'redis_server_search_fields_geo_Geo',
    'redis_server_search_fields_geo_Sortable': 'redis_server_search_fields_geo_Sortable',
    'redis_server_search_fields_geo_NoIndex': 'redis_server_search_fields_geo_NoIndex',
    'redis_server_search_fields_vector_Vector': 'redis_server_search_fields_vector_Vector',
    'redis_server_search_fields_vector_Flat': 'redis_server_search_fields_vector_Flat',
    'redis_server_search_fields_vector_HNSW': 'redis_server_search_fields_vector_HNSW',
    'redis_server_search_fields_geoshape_Geoshape': 'redis_server_search_fields_geoshape_Geoshape',
    'redis_server_search_fields_geoshape_Sortable': 'redis_server_search_fields_geoshape_Sortable',
    'redis_server_search_fields_geoshape_NoIndex': 'redis_server_search_fields_geoshape_NoIndex',
    'redis_server_search_fields__IndexErrors': 'redis_server_search_fields__IndexErrors',
    'redis_server_search_used_memory_indexes': 'redis_server_search_used_memory_indexes',
    'redis_server_search_smallest_memory_index': 'redis_server_search_smallest_memory_index',
    'redis_server_search_largest_memory_index': 'redis_server_search_largest_memory_index',
    'redis_server_search_total_indexing_time': 'redis_server_search_total_indexing_time',
    'redis_server_search_used_memory_vector_index': 'redis_server_search_used_memory_vector_index',
    'redis_server_search_global_idle': 'redis_server_search_global_idle',
    'redis_server_search_global_total': 'redis_server_search_global_total',
    'redis_server_search_bytes_collected': 'redis_server_search_bytes_collected',
    'redis_server_search_total_cycles': 'redis_server_search_total_cycles',
    'redis_server_search_total_ms_run': 'redis_server_search_total_ms_run',
    'redis_server_search_total_docs_not_collected_by_gc': 'redis_server_search_total_docs_not_collected_by_gc',
    'redis_server_search_marked_deleted_vectors': 'redis_server_search_marked_deleted_vectors',
    'redis_server_search_total_queries_processed': 'redis_server_search_total_queries_processed',
    'redis_server_search_total_query_commands': 'redis_server_search_total_query_commands',
    'redis_server_search_total_query_execution_time_ms': 'redis_server_search_total_query_execution_time_ms',
    'redis_server_search_total_active_queries': 'redis_server_search_total_active_queries',
    'redis_server_search_errors_indexing_failures': 'redis_server_search_errors_indexing_failures',
    'redis_server_search_errors_for_index_with_max_failures': 'redis_server_search_errors_for_index_with_max_failures',
}

DEFAULT_METRICS = [
    REDIS_CLUSTER,
    REDIS_DATABASE,
    REDIS_NODE,
    REDIS_SHARD,
    REDIS_INFO,
]

ADDITIONAL_METRICS = {
    'REDIS2.REPLICATION': REDIS_REPLICATION,
    'REDIS2.SHARDREPL': REDIS_SHARD_REPLICATION,
    'REDIS2.LDAP': REDIS_LDAP,
    'REDIS2.NETWORK': REDIS_NETWORK,
    'REDIS2.MEMORY': REDIS_MEMORY,
    'REDIS2.X509': REDIS_X509,
    'REDIS2.DISK': REDIS_DISK,
    'REDIS2.FILESYSTEM': REDIS_FILESYSTEM,
    'REDIS2.PROCESS': REDIS_PROCESS,
    'REDIS2.PRESSURE': REDIS_PRESSURE,
    'REDIS2.SEARCH': REDIS_SEARCH,
}
