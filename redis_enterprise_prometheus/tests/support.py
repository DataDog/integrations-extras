import os

from datadog_checks.dev import get_docker_hostname

VERSION = os.getenv('rdse2.redis_VERSION')
CHECK = 'rdse2.redis_enterprise_prometheus'

PORT = 8070
CONFTEST_PORT = 8443
HOST = get_docker_hostname()

ENDPOINT = "https://{}:{}/v2".format(HOST, PORT)
INSTANCE = {'openmetrics_endpoint': ENDPOINT}

CONFTEST = "https://{}:{}/#/bootstrap".format(HOST, CONFTEST_PORT)

ERSATZ_INSTANCE = {'openmetrics_endpoint': "https://localhost:8071/v2", 'tags': ['instance']}

EPHEMERAL = [
    'rdse2.node_available_flash_bytes',  # only present flash
    'rdse2.node_available_flash_no_overbooking_bytes',  # only present flash
    'rdse2.node_bigstore_free_bytes',  # only present bigstore
    'rdse2.node_provisional_flash_bytes',  # only present flash
    'rdse2.node_provisional_flash_no_overbooking_bytes',  # only present flash
    'rdse2.process_max_fds',
    'rdse2.process_open_fds',
    'rdse2.process_resident_memory_bytes',
    'rdse2.process_start_time_seconds',
    'rdse2.process_virtual_memory_bytes',
    'rdse2.process_virtual_memory_max_bytes',
    ### until we have added the following metrics to metrics.txt these must be ephemeral ###
    'rdse2.redis_server_search_number_of_active_indexes',
    'rdse2.redis_server_search_number_of_active_indexes_running_queries',
    'rdse2.redis_server_search_number_of_active_indexes_indexing',
    'rdse2.redis_server_search_total_active_write_threads',
    'rdse2.redis_server_search_fields_text_Sortable',
    'rdse2.redis_server_search_fields_text_NoIndex',
    'rdse2.redis_server_search_fields_numeric_Sortable',
    'rdse2.redis_server_search_fields_numeric_NoIndex',
    'rdse2.redis_server_search_fields_tag_Sortable',
    'rdse2.redis_server_search_fields_tag_NoIndex',
    'rdse2.redis_server_search_fields_tag_CaseSensitive',
    'rdse2.redis_server_search_fields_geo_Sortable',
    'rdse2.redis_server_search_fields_geo_NoIndex',
    'rdse2.redis_server_search_fields_vector_Flat',
    'rdse2.redis_server_search_fields_geoshape_Geoshape',
    'rdse2.redis_server_search_fields_geoshape_Sortable',
    'rdse2.redis_server_search_fields_geoshape_NoIndex',
    'rdse2.redis_server_search_fields__IndexErrors',
    'rdse2.redis_server_search_smallest_memory_index',
    'rdse2.redis_server_search_largest_memory_index',
    'rdse2.redis_server_search_used_memory_vector_index',
    'rdse2.redis_server_search_total_docs_not_collected_by_gc',
    'rdse2.redis_server_search_marked_deleted_vectors',
    'rdse2.redis_server_search_total_queries_processed',
    'rdse2.redis_server_search_total_query_commands',
    'rdse2.redis_server_search_total_query_execution_time_ms',
    'rdse2.redis_server_search_total_active_queries',
    'rdse2.redis_server_search_errors_indexing_failures',
    'rdse2.redis_server_search_errors_for_index_with_max_failures',
],

# enterprise metrics use the namespace 'rdse'
METRICS_MAP = {
    'REDIS2.CLUSTER': [
        'rdse2.generation',
        'rdse2.has_quorum',
        'rdse2.is_primary',
        # 'rdse2.license_shards_limit',
        'rdse2.total_live_nodes_count',
        'rdse2.total_nodes_count',
    ],
    'REDIS2.DATABASE': [
        # 'rdse2.db_config',
        'rdse2.db_memory_limit_bytes',
        # 'rdse2.db_status',
        'rdse2.endpoint_client_connection_expired.count',
        'rdse2.endpoint_client_connections.count',
        'rdse2.endpoint_client_disconnections.count',
        'rdse2.endpoint_client_establishment_failures.count',
        'rdse2.endpoint_client_tracking_off_requests.count',
        'rdse2.endpoint_client_tracking_on_requests.count',
        'rdse2.endpoint_dedicated_sconn_connections.count',
        'rdse2.endpoint_dedicated_sconn_proxy_disconnections.count',
        'rdse2.endpoint_dedicated_sconn_shard_disconnections.count',
        'rdse2.endpoint_disposed_commands_after_client_caching.count',
        'rdse2.endpoint_egress.count',
        'rdse2.endpoint_egress_pending.count',
        'rdse2.endpoint_egress_pending_discarded.count',
        'rdse2.endpoint_ingress.count',
        'rdse2.endpoint_internal_client_connections.count',
        'rdse2.endpoint_internal_client_disconnections.count',
        'rdse2.endpoint_internal_proxy_disconnections.count',
        'rdse2.endpoint_other_requests.count',
        'rdse2.endpoint_other_requests_latency_histogram.sum',
        'rdse2.endpoint_other_requests_latency_histogram.count',
        'rdse2.endpoint_other_requests_latency_histogram.bucket',
        'rdse2.endpoint_other_responses.count',
        'rdse2.endpoint_proxy_disconnections.count',
        'rdse2.endpoint_read_requests.count',
        'rdse2.endpoint_read_requests_latency_histogram.sum',
        'rdse2.endpoint_read_requests_latency_histogram.count',
        'rdse2.endpoint_read_requests_latency_histogram.bucket',
        'rdse2.endpoint_read_responses.count',
        'rdse2.endpoint_sconn_application_handshake_failure.count',
        'rdse2.endpoint_sconn_establishment_failure.count',
        'rdse2.endpoint_shared_sconn_connections.count',
        'rdse2.endpoint_shared_sconn_proxy_disconnections.count',
        'rdse2.endpoint_shared_sconn_shard_disconnections.count',
        'rdse2.endpoint_write_requests.count',
        'rdse2.endpoint_write_requests_latency_histogram.sum',
        'rdse2.endpoint_write_requests_latency_histogram.count',
        'rdse2.endpoint_write_requests_latency_histogram.bucket',
        'rdse2.endpoint_write_responses.count',
    ],
    'REDIS2.NODE': [
        'rdse2.node_available_flash_bytes',
        'rdse2.node_available_flash_no_overbooking_bytes',
        'rdse2.node_available_memory_bytes',
        'rdse2.node_available_memory_no_overbooking_bytes',
        'rdse2.node_bigstore_free_bytes',
        'rdse2.x509_cert_expires_in_seconds',
        'rdse2.x509_exporter_build_info',
        'rdse2.x509_read_errors',
        'rdse2.x509_cert_valid_since_seconds',
        'rdse2.x509_cert_not_before',
        'rdse2.x509_cert_not_after',
        'rdse2.x509_cert_expired',
        'rdse2.node_ephemeral_storage_avail_bytes',
        'rdse2.node_ephemeral_storage_free_bytes',
        'rdse2.node_memory_MemFree_bytes',
        'rdse2.node_persistent_storage_avail_bytes',
        'rdse2.node_persistent_storage_free_bytes',
        'rdse2.node_provisional_flash_bytes',
        'rdse2.node_provisional_flash_no_overbooking_bytes',
        'rdse2.node_provisional_memory_bytes',
        'rdse2.node_provisional_memory_no_overbooking_bytes',
        'rdse2.node_metrics_up',
    ],
    'REDIS2.SHARD': [
        'rdse2.redis_server_active_defrag_running',
        'rdse2.redis_server_allocator_active',
        'rdse2.redis_server_allocator_allocated',
        'rdse2.redis_server_allocator_resident',
        'rdse2.redis_server_aof_last_cow_size',
        'rdse2.redis_server_aof_rewrite_in_progress',
        'rdse2.redis_server_aof_rewrites',
        'rdse2.redis_server_aof_delayed_fsync',
        'rdse2.redis_server_blocked_clients',
        'rdse2.redis_server_connected_clients',
        'rdse2.redis_server_connected_slaves',
        'rdse2.redis_server_db0_avg_ttl',
        'rdse2.redis_server_expired_keys',
        'rdse2.redis_server_db0_keys',
        'rdse2.redis_server_evicted_keys',
        'rdse2.redis_server_expire_cycle_cpu_milliseconds',
        'rdse2.redis_server_expired_keys',
        'rdse2.redis_server_forwarding_state',
        'rdse2.redis_server_keys_trimmed',
        'rdse2.redis_server_keyspace_read_hits',
        'rdse2.redis_server_keyspace_read_misses',
        'rdse2.redis_server_keyspace_write_hits',
        'rdse2.redis_server_keyspace_write_misses',
        'rdse2.redis_server_master_link_status',
        'rdse2.redis_server_master_repl_offset',
        'rdse2.redis_server_master_sync_in_progress',
        'rdse2.redis_server_max_process_mem',
        'rdse2.redis_server_maxmemory',
        'rdse2.redis_server_mem_aof_buffer',
        'rdse2.redis_server_mem_clients_normal',
        'rdse2.redis_server_mem_clients_slaves',
        'rdse2.redis_server_mem_fragmentation_ratio',
        'rdse2.redis_server_mem_not_counted_for_evict',
        'rdse2.redis_server_mem_replication_backlog',
        'rdse2.redis_server_module_fork_in_progress',
        'rdse2.namedprocess_namegroup_cpu_seconds.count',
        'rdse2.namedprocess_namegroup_thread_cpu_seconds.count',
        'rdse2.namedprocess_namegroup_open_filedesc',
        'rdse2.namedprocess_namegroup_memory_bytes',
        'rdse2.namedprocess_namegroup_oldest_start_time_seconds',
        'rdse2.redis_server_rdb_bgsave_in_progress',
        'rdse2.redis_server_rdb_last_cow_size',
        'rdse2.redis_server_rdb_saves',
        'rdse2.redis_server_repl_touch_bytes',
        'rdse2.redis_server_total_commands_processed',
        'rdse2.redis_server_total_connections_received',
        'rdse2.redis_server_total_net_input_bytes',
        'rdse2.redis_server_total_net_output_bytes',
        'rdse2.redis_server_up',
        'rdse2.redis_server_used_memory',
    ],
    'REDIS2.INFO': [
        'rdse2.node_dmi_info',
        'rdse2.node_os_info',
        'rdse2.node_disk_info',
    ],
    # END DEFAULT
    'REDIS2.REPLICATION': [
        'rdse2.database_syncer_config',
        'rdse2.database_syncer_current_status',
        'rdse2.database_syncer_dst_connectivity_state',
        'rdse2.database_syncer_dst_connectivity_state_ms',
        'rdse2.database_syncer_dst_lag',
        'rdse2.database_syncer_dst_repl_offset',
        'rdse2.database_syncer_flush_counter',
        'rdse2.database_syncer_ingress_bytes',
        'rdse2.database_syncer_ingress_bytes_decompressed',
        'rdse2.database_syncer_internal_state',
        'rdse2.database_syncer_lag_ms',
        'rdse2.database_syncer_rdb_size',
        'rdse2.database_syncer_rdb_transferred',
        'rdse2.database_syncer_src_connectivity_state',
        'rdse2.database_syncer_src_connectivity_state_ms',
        'rdse2.database_syncer_src_repl_offset',
        'rdse2.database_syncer_state',
        'rdse2.database_syncer_syncer_repl_offset',
        'rdse2.database_syncer_total_requests',
        'rdse2.database_syncer_total_responses',
    ],
    'REDIS2.SHARDREPL': [
        'rdse2.redis_crdt_backlog_histlen',
        'rdse2.redis_crdt_backlog_idx',
        'rdse2.redis_crdt_backlog_master_offset',
        'rdse2.redis_crdt_backlog_offset',
        'rdse2.redis_crdt_backlog_refs',
        'rdse2.redis_crdt_backlog_size',
        'rdse2.redis_crdt_clock',
        'rdse2.redis_crdt_effect_reqs',
        'rdse2.redis_crdt_gc_attempted',
        'rdse2.redis_crdt_gc_collected',
        'rdse2.redis_crdt_gc_elements_attempted',
        'rdse2.redis_crdt_gc_elements_collected',
        'rdse2.redis_crdt_gc_pending',
        'rdse2.redis_crdt_gc_skipped',
        'rdse2.redis_crdt_key_headers',
        'rdse2.redis_crdt_list_trimmed_vertices',
        'rdse2.redis_crdt_merge_reqs',
        'rdse2.redis_crdt_oom_latch',
        'rdse2.redis_crdt_ovc_filtered_effect_reqs',
        'rdse2.redis_crdt_peer_dst_id',
        'rdse2.redis_crdt_peer_id',
        'rdse2.redis_crdt_peer_lag',
        'rdse2.redis_crdt_peer_offset',
        'rdse2.redis_crdt_peer_peer_state',
        'rdse2.redis_crdt_pending_list_trimmed_vertices',
        'rdse2.redis_crdt_raw_dbsize',
        'rdse2.redis_crdt_replica_config_version',
        'rdse2.redis_crdt_replica_max_ops_lag',
        'rdse2.redis_crdt_replica_min_ops_lag',
        'rdse2.redis_crdt_replica_shards',
        'rdse2.redis_crdt_replica_slot_coverage_by_any_ovc',
        'rdse2.redis_crdt_replica_slot_coverage_by_only_ovc',
        'rdse2.redis_crdt_replica_slots',
        'rdse2.redis_crdt_stale_replica',
        'rdse2.redis_crdt_ts_key_headers',
    ],
    'REDIS2.LDAP': [
        'rdse2.directory_cache_hits.count',
        'rdse2.directory_cache_miss_then_hits.count',
        'rdse2.directory_cache_misses.count',
        'rdse2.directory_cache_refreshes.count',
        'rdse2.directory_cache_stales.count',
        'rdse2.directory_conn_connections.count',
        'rdse2.directory_conn_disconnections.count',
        'rdse2.directory_conn_failed_connections.count',
        'rdse2.directory_queries_error.count',
        'rdse2.directory_queries_expired.count',
        'rdse2.directory_queries_no_conn.count',
        'rdse2.directory_queries_sent.count',
        'rdse2.directory_queries_success.count',
        'rdse2.directory_queries_wrongpass.count',
        'rdse2.directory_requests.count',
    ],
    'REDIS2.NETWORK': [
        'rdse2.node_network_receive_bytes.count',
        'rdse2.node_network_receive_compressed.count',
        'rdse2.node_network_receive_drop.count',
        'rdse2.node_network_receive_errs.count',
        'rdse2.node_network_receive_fifo.count',
        'rdse2.node_network_receive_frame.count',
        'rdse2.node_network_receive_multicast.count',
        'rdse2.node_network_receive_nohandler.count',
        'rdse2.node_network_receive_packets.count',
        'rdse2.node_network_transmit_bytes.count',
        'rdse2.node_network_transmit_carrier.count',
        'rdse2.node_network_transmit_colls.count',
        'rdse2.node_network_transmit_compressed.count',
        'rdse2.node_network_transmit_drop.count',
        'rdse2.node_network_transmit_errs.count',
        'rdse2.node_network_transmit_fifo.count',
        'rdse2.node_network_transmit_packets.count',
    ],
    'REDIS2.MEMORY': [
        'rdse2.node_memory_Active_anon_bytes',
        'rdse2.node_memory_Active_bytes',
        'rdse2.node_memory_Active_file_bytes',
        'rdse2.node_memory_AnonHugePages_bytes',
        'rdse2.node_memory_AnonPages_bytes',
        'rdse2.node_memory_Bounce_bytes',
        'rdse2.node_memory_Buffers_bytes',
        'rdse2.node_memory_Cached_bytes',
        'rdse2.node_memory_CommitLimit_bytes',
        'rdse2.node_memory_Committed_AS_bytes',
        'rdse2.node_memory_DirectMap1G_bytes',
        'rdse2.node_memory_DirectMap2M_bytes',
        'rdse2.node_memory_DirectMap4k_bytes',
        'rdse2.node_memory_Dirty_bytes',
        'rdse2.node_memory_FileHugePages_bytes',
        'rdse2.node_memory_FilePmdMapped_bytes',
        'rdse2.node_memory_HardwareCorrupted_bytes',
        'rdse2.node_memory_HugePages_Free',
        'rdse2.node_memory_HugePages_Rsvd',
        'rdse2.node_memory_HugePages_Surp',
        'rdse2.node_memory_HugePages_Total',
        'rdse2.node_memory_Hugepagesize_bytes',
        'rdse2.node_memory_Hugetlb_bytes',
        'rdse2.node_memory_Inactive_anon_bytes',
        'rdse2.node_memory_Inactive_bytes',
        'rdse2.node_memory_Inactive_file_bytes',
        'rdse2.node_memory_KReclaimable_bytes',
        'rdse2.node_memory_KernelStack_bytes',
        'rdse2.node_memory_Mapped_bytes',
        'rdse2.node_memory_MemAvailable_bytes',
        'rdse2.node_memory_MemFree_bytes',
        'rdse2.node_memory_MemTotal_bytes',
        'rdse2.node_memory_Mlocked_bytes',
        'rdse2.node_memory_NFS_Unstable_bytes',
        'rdse2.node_memory_PageTables_bytes',
        'rdse2.node_memory_Percpu_bytes',
        'rdse2.node_memory_SReclaimable_bytes',
        'rdse2.node_memory_SUnreclaim_bytes',
        'rdse2.node_memory_ShmemHugePages_bytes',
        'rdse2.node_memory_ShmemPmdMapped_bytes',
        'rdse2.node_memory_Shmem_bytes',
        'rdse2.node_memory_Slab_bytes',
        'rdse2.node_memory_SwapCached_bytes',
        'rdse2.node_memory_SwapFree_bytes',
        'rdse2.node_memory_SwapTotal_bytes',
        'rdse2.node_memory_Unevictable_bytes',
        'rdse2.node_memory_VmallocChunk_bytes',
        'rdse2.node_memory_VmallocTotal_bytes',
        'rdse2.node_memory_VmallocUsed_bytes',
        'rdse2.node_memory_WritebackTmp_bytes',
        'rdse2.node_memory_Writeback_bytes',
    ],
    'REDIS2.X509': [
        'rdse2.x509_cert_expired',
        'rdse2.x509_cert_expires_in_seconds',
        'rdse2.x509_cert_not_after',
        'rdse2.x509_cert_not_before',
        'rdse2.x509_cert_valid_since_seconds',
        'rdse2.x509_exporter_build_info',
        'rdse2.x509_read_errors',
    ],
    'REDIS2.DISK': [
        'rdse2.node_disk_discard_time_seconds.count',
        'rdse2.node_disk_discarded_sectors.count',
        'rdse2.node_disk_discards_completed.count',
        'rdse2.node_disk_discards_merged.count',
        'rdse2.node_disk_flush_requests_time_seconds.count',
        'rdse2.node_disk_flush_requests.count',
        'rdse2.node_disk_io_now',
        'rdse2.node_disk_io_time_seconds.count',
        'rdse2.node_disk_io_time_weighted_seconds.count',
        'rdse2.node_disk_read_bytes.count',
        'rdse2.node_disk_read_time_seconds.count',
        'rdse2.node_disk_reads_completed.count',
        'rdse2.node_disk_reads_merged.count',
        'rdse2.node_disk_write_time_seconds.count',
        'rdse2.node_disk_writes_completed.count',
        'rdse2.node_disk_writes_merged.count',
        'rdse2.node_disk_written_bytes.count',
    ],
    'REDIS2.FILESYSTEM': [
        'rdse2.node_filesystem_avail_bytes',
        'rdse2.node_filesystem_device_error',
        'rdse2.node_filesystem_files',
        'rdse2.node_filesystem_files_free',
        'rdse2.node_filesystem_free_bytes',
        'rdse2.node_filesystem_readonly',
        'rdse2.node_filesystem_size_bytes',
    ],
    'REDIS2.PROCESS': [
        'rdse2.process_exporter_build_info',
        'rdse2.node_processes_max_threads',
        'rdse2.node_processes_max_processes',
        'rdse2.node_processes_pids',
        'rdse2.node_processes_state',
        'rdse2.node_processes_threads',
        'rdse2.node_processes_threads_state',
    ],
    'REDIS2.PRESSURE': [
        'rdse2.node_pressure_cpu_waiting_seconds.count',
        'rdse2.node_pressure_io_stalled_seconds.count',
        'rdse2.node_pressure_io_waiting_seconds.count',
        'rdse2.node_pressure_memory_stalled_seconds.count',
        'rdse2.node_pressure_memory_waiting_seconds.count',
    ],
    'REDIS2.SEARCH': [
        'rdse2.redis_server_search_number_of_indexes',
        'rdse2.redis_server_search_number_of_active_indexes',
        'rdse2.redis_server_search_number_of_active_indexes_running_queries',
        'rdse2.redis_server_search_number_of_active_indexes_indexing',
        'rdse2.redis_server_search_total_active_write_threads',
        'rdse2.redis_server_search_fields_text_Text',
        'rdse2.redis_server_search_fields_text_Sortable',
        'rdse2.redis_server_search_fields_text_NoIndex',
        'rdse2.redis_server_search_fields_numeric_Numeric',
        'rdse2.redis_server_search_fields_numeric_Sortable',
        'rdse2.redis_server_search_fields_numeric_NoIndex',
        'rdse2.redis_server_search_fields_tag_Tag',
        'rdse2.redis_server_search_fields_tag_Sortable',
        'rdse2.redis_server_search_fields_tag_NoIndex',
        'rdse2.redis_server_search_fields_tag_CaseSensitive',
        'rdse2.redis_server_search_fields_geo_Geo',
        'rdse2.redis_server_search_fields_geo_Sortable',
        'rdse2.redis_server_search_fields_geo_NoIndex',
        'rdse2.redis_server_search_fields_vector_Vector',
        'rdse2.redis_server_search_fields_vector_Flat',
        'rdse2.redis_server_search_fields_vector_HNSW',
        'rdse2.redis_server_search_fields_geoshape_Geoshape',
        'rdse2.redis_server_search_fields_geoshape_Sortable',
        'rdse2.redis_server_search_fields_geoshape_NoIndex',
        'rdse2.redis_server_search_fields__IndexErrors',
        'rdse2.redis_server_search_used_memory_indexes',
        'rdse2.redis_server_search_smallest_memory_index',
        'rdse2.redis_server_search_largest_memory_index',
        'rdse2.redis_server_search_total_indexing_time',
        'rdse2.redis_server_search_used_memory_vector_index',
        'rdse2.redis_server_search_global_idle',
        'rdse2.redis_server_search_global_total',
        'rdse2.redis_server_search_bytes_collected',
        'rdse2.redis_server_search_total_cycles',
        'rdse2.redis_server_search_total_ms_run',
        'rdse2.redis_server_search_total_docs_not_collected_by_gc',
        'rdse2.redis_server_search_marked_deleted_vectors',
        'rdse2.redis_server_search_total_queries_processed',
        'rdse2.redis_server_search_total_query_commands',
        'rdse2.redis_server_search_total_query_execution_time_ms',
        'rdse2.redis_server_search_total_active_queries',
        'rdse2.redis_server_search_errors_indexing_failures',
        'rdse2.redis_server_search_errors_for_index_with_max_failures',
    ]
}

DEFAULT_METRICS = [
    'REDIS2.CLUSTER',
    'REDIS2.DATABASE',
    'REDIS2.NODE',
    'REDIS2.SHARD',
    'REDIS2.INFO',
]

ADDITIONAL_METRICS = [
    'REDIS2.REPLICATION',
    'REDIS2.SHARDREPL',
    'REDIS2.LDAP',
    'REDIS2.NETWORK',
    'REDIS2.MEMORY',
    'REDIS2.X509',
    'REDIS2.DISK',
    'REDIS2.FILESYSTEM',
    'REDIS2.PROCESS',
    'REDIS2.PRESSURE',
    'REDIS2.SEARCH',
]


def get_metrics(metric_groups):
    return sorted(m for g in metric_groups for m in DEFAULT_METRICS[g])
