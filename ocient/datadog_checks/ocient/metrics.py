METRIC_MAP = [
    {
        "ocient_lat_paused": {
            "name": "lat.paused"
        },
        "ocient_lat_bytes_buffered": {
            "name": "lat.bytes_buffered"
        },
        "ocient_lat_complete": {
            "name": "lat.complete"
        },
        "ocient_lat_workers": {
            "name": "lat.workers"
        },
        "ocient_lat_pipeline_bytes_pushed": {
            "name": "lat.pipeline.bytes_pushed"
        },
        "ocient_lat_pipeline_push_errors": {
            "name": "lat.pipeline.push_errors"
        },
        "ocient_lat_pipeline_push_attempts": {
            "name": "lat.pipeline.push_attempts"
        },
        "ocient_lat_pipeline_rows_pushed": {
            "name": "lat.pipeline.rows_pushed"
        },
        "ocient_lat_pipeline_record_errors": {
            "name": "lat.pipeline.record_errors"
        },
        "ocient_allocation_pending_timeouts": {
            "name": "allocation.pending_timeouts"
        },
        "ocient_blobstore_num_blobs": {
            "name": "blobstore.num_blobs"
        },
        "ocient_blobstore_pending_dispatches": {
            "name": "blobstore.pending_dispatches"
        },
        "ocient_blobstore_total_bytes": {
            "name": "blobstore.total_bytes"
        },
        "ocient_blobstore_verify_hash_operations": {
            "name": "blobstore.verify_hash_operations"
        },
        "ocient_blockDeviceContext_bytesRead": {
            "name": "blockDeviceContext.bytesRead"
        },
        "ocient_cmdcomp_metadata_cache_operations": {
            "name": "cmdcomp.metadata.cache_operations"
        },
        "ocient_cmdcomp_metadata_eviction_cycles": {
            "name": "cmdcomp.metadata.eviction_cycles"
        },
        "ocient_cmdcomp_metadata_tableToRequestStatsCounter": {
            "name": "cmdcomp.metadata.tableToRequestStatsCounter"
        },
        "ocient_cmdcomp_queries": {
            "name": "cmdcomp.queries"
        },
        "ocient_cmdcomp_sql_node_load": {
            "name": "cmdcomp.sql_node_load"
        },
        "ocient_cmdcomps_server_connections": {
            "name": "cmdcomps.server_connections"
        },
        "ocient_disk_based_operator_instance_bytes_spilled_compressed": {
            "name": "disk_based_operator_instance.bytes_spilled_compressed"
        },
        "ocient_disk_based_operator_instance_bytes_spilled_uncompressed": {
            "name": "disk_based_operator_instance.bytes_spilled_uncompressed"
        },
        "ocient_fs_num_file_instances": {
            "name": "fs.num_file_instances"
        },
        "ocient_fs_num_loaded_inode_descriptor_blocks": {
            "name": "fs.num_loaded_inode_descriptor_blocks"
        },
        "ocient_fs_num_memory_stalls": {
            "name": "fs.num_memory_stalls"
        },
        "ocient_fs_operations": {
            "name": "fs.operations"
        },
        "ocient_fs_volume_fragmentation_avg": {
            "name": "fs.volume.fragmentation.avg"
        },
        "ocient_fs_volume_fragmentation_max": {
            "name": "fs.volume.fragmentation.max"
        },
        "ocient_fs_volume_fragmentation_min": {
            "name": "fs.volume.fragmentation.min"
        },
        "ocient_fs_volume_free_bytes": {
            "name": "fs.volume.free_bytes"
        },
        "ocient_fs_volume_free_blocks": {
            "name": "fs.volume.free_blocks"
        },
        "ocient_fs_volume_free_inodes": {
            "name": "fs.volume.free_inodes"
        },
        "ocient_fs_volume_health_status": {
            "name": "fs.volume.health.status"
        },
        "ocient_fs_volume_inodeOperationsSize": {
            "name": "fs.volume.inodeOperationsSize"
        },
        "ocient_fs_volume_legacySpaceUsedPct": {
            "name": "fs.volume.legacySpaceUsedPct"
        },
        "ocient_fs_volume_outstanding_operations": {
            "name": "fs.volume.outstanding_operations"
        },
        "ocient_fs_volume_space_used_pct": {
            "name": "fs.volume.space_used_pct"
        },
        "ocient_fs_volume_total_blocks": {
            "name": "fs.volume.total_blocks"
        },
        "ocient_fs_volume_total_blocks_used": {
            "name": "fs.volume.total_blocks_used"
        },
        "ocient_fs_volume_total_bytes": {
            "name": "fs.volume.total_bytes"
        },
        "ocient_fs_volume_total_bytes_used": {
            "name": "fs.volume.total_bytes_used"
        },
        "ocient_fs_volume_total_inodes": {
            "name": "fs.volume.total_inodes"
        },
        "ocient_fs_volume_total_inodes_used": {
            "name": "fs.volume.total_inodes_used"
        },
        "ocient_fs_volume_health_corruptions": {
            "name": "fs.volume_health.corruptions"
        },
        "ocient_gsd_buffer_batched_requests_avg": {
            "name": "gsd_buffer.batched_requests.avg"
        },
        "ocient_healthProtocolInstance_numRunningTasks": {
            "name": "healthProtocolInstance.numRunningTasks"
        },
        "ocient_io_page_scheduler_page_count": {
            "name": "io.page_scheduler.page_count"
        },
        "ocient_jemalloc_stats": {
            "name": "jemalloc.stats"
        },
        "ocient_loadTocLimit_pendingQueueCount": {
            "name": "loadTocLimit.pendingQueueCount"
        },
        "ocient_local_storage_service_available_spare_pct": {
            "name": "local_storage_service.available_spare_pct"
        },
        "ocient_local_storage_service_controller_busy_time": {
            "name": "local_storage_service.controller_busy_time"
        },
        "ocient_local_storage_service_crc_errors": {
            "name": "local_storage_service.crc_errors"
        },
        "ocient_local_storage_service_data_units_write": {
            "name": "local_storage_service.data_units_write"
        },
        "ocient_local_storage_service_device_endurance": {
            "name": "local_storage_service.device_endurance"
        },
        "ocient_local_storage_service_device_status": {
            "name": "local_storage_service.device_status"
        },
        "ocient_local_storage_service_error_log_entries": {
            "name": "local_storage_service.error_log_entries"
        },
        "ocient_local_storage_service_free_space": {
            "name": "local_storage_service.free_space"
        },
        "ocient_local_storage_service_media_errors": {
            "name": "local_storage_service.media_errors"
        },
        "ocient_local_storage_service_opal_enabled": {
            "name": "local_storage_service.opal_enabled"
        },
        "ocient_local_storage_service_opal_status": {
            "name": "local_storage_service.opal_status"
        },
        "ocient_local_storage_service_opal_supported": {
            "name": "local_storage_service.opal_supported"
        },
        "ocient_local_storage_service_operations": {
            "name": "local_storage_service.operations"
        },
        "ocient_local_storage_service_power_cycles": {
            "name": "local_storage_service.power_cycles"
        },
        "ocient_local_storage_service_power_on_hours": {
            "name": "local_storage_service.power_on_hours"
        },
        "ocient_local_storage_service_read_commands": {
            "name": "local_storage_service.read_commands"
        },
        "ocient_local_storage_service_segment_table_entries": {
            "name": "local_storage_service.segment_table_entries"
        },
        "ocient_local_storage_service_space_free_pct": {
            "name": "local_storage_service.space_free_pct"
        },
        "ocient_local_storage_service_temp": {
            "name": "local_storage_service.temp"
        },
        "ocient_local_storage_service_total_space": {
            "name": "local_storage_service.total_space"
        },
        "ocient_local_storage_service_unsafe_shutdowns": {
            "name": "local_storage_service.unsafe_shutdowns"
        },
        "ocient_local_storage_service_warn_available_spare": {
            "name": "local_storage_service.warn_available_spare"
        },
        "ocient_local_storage_service_warn_read_only": {
            "name": "local_storage_service.warn_read_only"
        },
        "ocient_local_storage_service_warn_reliability": {
            "name": "local_storage_service.warn_reliability"
        },
        "ocient_local_storage_service_warn_temp": {
            "name": "local_storage_service.warn_temp"
        },
        "ocient_local_storage_service_write_block_complete": {
            "name": "local_storage_service.write_block_complete"
        },
        "ocient_local_storage_service_write_block_count": {
            "name": "local_storage_service.write_block_count"
        },
        "ocient_local_storage_service_write_commands": {
            "name": "local_storage_service.write_commands"
        },
        "ocient_local_storage_service_write_complete": {
            "name": "local_storage_service.write_complete"
        },
        "ocient_local_storage_service_write_submit_count": {
            "name": "local_storage_service.write_submit_count"
        },
        "ocient_memory_heap": {
            "name": "memory.heap"
        },
        "ocient_memory_huge": {
            "name": "memory.huge"
        },
        "ocient_metadata_storage_protocol_task_count": {
            "name": "metadata.storage_protocol.task_count"
        },
        "ocient_metadata_storage_protocol_task_time_avg": {
            "name": "metadata.storage_protocol.task_time.avg"
        },
        "ocient_metadataStorageProtocolInstance_lastDeserializationDuration": {
            "name": "metadataStorageProtocolInstance.lastDeserializationDuration"
        },
        "ocient_metadataStorageProtocolInstance_lastSerializationConfigSize": {
            "name": "metadataStorageProtocolInstance.lastSerializationConfigSize"
        },
        "ocient_metadataStorageProtocolInstance_lastSerializationDuration": {
            "name": "metadataStorageProtocolInstance.lastSerializationDuration"
        },
        "ocient_network_tcpChannel_uvBufferPool_bytesInUse": {
            "name": "network.tcpChannel.uvBufferPool.bytesInUse"
        },
        "ocient_db_can_connect": {
            "name": "db.can_connect"
        },
        "ocient_db_gdc_current_count": {
            "name": "db.gdc_current_count"
        },
        "ocient_db_gdc_max_count": {
            "name": "db.gdc_max_count"
        },
        "ocient_db_maxpagetime": {
            "name": "db.maxpagetime"
        },
        "ocient_db_maxsegtime": {
            "name": "db.maxsegtime"
        },
        "ocient_db_minpagetime": {
            "name": "db.minpagetime"
        },
        "ocient_db_minsegtime": {
            "name": "db.minsegtime"
        },
        "ocient_db_page_rows": {
            "name": "db.page_rows"
        },
        "ocient_db_pagecount": {
            "name": "db.pagecount"
        },
        "ocient_db_query_count": {
            "name": "db.query_count"
        },
        "ocient_db_rows_per_page": {
            "name": "db.rows_per_page"
        },
        "ocient_db_rows_per_seg": {
            "name": "db.rows_per_seg"
        },
        "ocient_db_seg_rows": {
            "name": "db.seg_rows"
        },
        "ocient_db_segcount": {
            "name": "db.segcount"
        },
        "ocient_db_segments": {
            "name": "db.segments"
        },
        "ocient_db_size": {
            "name": "db.size"
        },
        "ocient_db_tot_rows": {
            "name": "db.tot_rows"
        },
        "ocient_operator_summary_num_operators": {
            "name": "operator_summary.num_operators"
        },
        "ocient_operator_summary_num_queries": {
            "name": "operator_summary.num_queries"
        },
        "ocient_operator_summary_oldest_age": {
            "name": "operator_summary.oldest_age"
        },
        "ocient_partitionProvider_lockSlotsTotal": {
            "name": "partitionProvider.lockSlotsTotal"
        },
        "ocient_partitionProvider_lockSlotsUsed": {
            "name": "partitionProvider.lockSlotsUsed"
        },
        "ocient_partition_provider_bytes_read": {
            "name": "partition_provider.bytes_read"
        },
        "ocient_partition_provider_cache_bytes": {
            "name": "partition_provider.cache_bytes"
        },
        "ocient_partition_provider_cache_operations": {
            "name": "partition_provider.cache_operations"
        },
        "ocient_partition_provider_cache_raw_bytes": {
            "name": "partition_provider.cache_raw_bytes"
        },
        "ocient_partition_provider_cache_size": {
            "name": "partition_provider.cache_size"
        },
        "ocient_protocol_actions": {
            "name": "protocol.actions"
        },
        "ocient_protocol_actions_count": {
            "name": "protocol.actions.count"
        },
        "ocient_protocol_actions_time": {
            "name": "protocol.actions.time"
        },
        "ocient_protocol_cached_rows": {
            "name": "protocol.cached_rows"
        },
        "ocient_protocol_cached_tables": {
            "name": "protocol.cached_tables"
        },
        "ocient_protocol_raft_participant_state": {
            "name": "protocol.raft.participant_state"
        },
        "ocient_protocol_raft_snapshot_size": {
            "name": "protocol.raft.snapshot_size"
        },
        "ocient_protocol_time": {
            "name": "protocol.time"
        },
        "ocient_raftEngine_metadataStorageProtocol_nodeCameOnline_time": {
            "name": "raftEngine.metadataStorageProtocol.nodeCameOnline.time"
        },
        "ocient_resource_manager_pending_hp_memory": {
            "name": "resource_manager.pending_hp_memory"
        },
        "ocient_result_cache_queries": {
            "name": "result_cache.queries"
        },
        "ocient_rolehostd_initialization_status": {
            "name": "rolehostd.initialization_status"
        },
        "ocient_segment_activation_limit_pending_queue_count": {
            "name": "segment_activation_limit.pending_queue_count"
        },
        "ocient_segment_store_bytes": {
            "name": "segment_store.bytes"
        },
        "ocient_segment_store_count": {
            "name": "segment_store.count"
        },
        "ocient_segment_store_operations": {
            "name": "segment_store.operations"
        },
        "ocient_segment_transfer_operations_count": {
            "name": "segment_transfer.operations.count"
        },
        "ocient_segment_transfer_operations_duration": {
            "name": "segment_transfer.operations.duration"
        },
        "ocient_storage_cluster_activating_segments": {
            "name": "storage_cluster.activating_segments"
        },
        "ocient_storage_cluster_data_stats_avg_row_count": {
            "name": "storage_cluster.data_stats.avg_row_count"
        },
        "ocient_storage_cluster_data_stats_avg_size": {
            "name": "storage_cluster.data_stats.avg_size"
        },
        "ocient_storage_cluster_data_stats_num_objects": {
            "name": "storage_cluster.data_stats.num_objects"
        },
        "ocient_storage_cluster_data_stats_total_row_count": {
            "name": "storage_cluster.data_stats.total_row_count"
        },
        "ocient_storage_cluster_data_stats_total_size": {
            "name": "storage_cluster.data_stats.total_size"
        },
        "ocient_storage_cluster_node_table_segment_size_lookup_size": {
            "name": "storage_cluster.node_table_segment_size_lookup.size"
        },
        "ocient_storage_cluster_on_put_segment_data_throughput_avg": {
            "name": "storage_cluster.on_put_segment_data.throughput.avg"
        },
        "ocient_storage_cluster_osn_reaps_batched": {
            "name": "storage_cluster.osn_reaps.batched"
        },
        "ocient_storage_cluster_osn_reaps_duration": {
            "name": "storage_cluster.osn_reaps.duration"
        },
        "ocient_storage_cluster_osns_created": {
            "name": "storage_cluster.osns.created"
        },
        "ocient_storage_cluster_osns_reaped": {
            "name": "storage_cluster.osns.reaped"
        },
        "ocient_storage_cluster_pending_segment_deletions": {
            "name": "storage_cluster.pending_segment_deletions"
        },
        "ocient_storage_cluster_probes_complete": {
            "name": "storage_cluster.probes.complete"
        },
        "ocient_storage_cluster_probes_incomplete": {
            "name": "storage_cluster.probes.incomplete"
        },
        "ocient_storage_storage_elapsed_time_for_first_osn_to_activate": {
            "name": "storage_storage.elapsed_time_for_first_osn_to_activate"
        },
        "ocient_storage_table_action_cooldown_buffer_queued_actions": {
            "name": "storage_table_action_cooldown_buffer.queued_actions"
        },
        "ocient_stream_loader_api_push_rows_requests": {
            "name": "stream_loader.api.push_rows_requests"
        },
        "ocient_stream_loader_data_page_max_size": {
            "name": "stream_loader.data.page_max_size"
        },
        "ocient_stream_loader_data_page_median_count": {
            "name": "stream_loader.data.page_median_count"
        },
        "ocient_stream_loader_data_page_min_size": {
            "name": "stream_loader.data.page_min_size"
        },
        "ocient_stream_loader_data_tracked_page_bytes": {
            "name": "stream_loader.data.tracked_page_bytes"
        },
        "ocient_stream_loader_data_tracked_page_count": {
            "name": "stream_loader.data.tracked_page_count"
        },
        "ocient_tkt_pipeline_operations": {
            "name": "tkt.pipeline.operations"
        },
        "ocient_tkt_segment_service_cache_ops": {
            "name": "tkt.segment_service.cache_ops"
        },
        "ocient_tkt_segment_service_cache_size": {
            "name": "tkt.segment_service.cache_size"
        },
        "ocient_tkt_segment_service_required_tables": {
            "name": "tkt.segment_service.required_tables"
        },
        "ocient_virtual_read_cache_back_writes": {
            "name": "virtual_read_cache.back_writes"
        },
        "ocient_virtual_read_cache_disk_operations": {
            "name": "virtual_read_cache.disk.operations"
        },
        "ocient_virtual_read_cache_heap_operations": {
            "name": "virtual_read_cache.heap.operations"
        },
        "ocient_virtual_read_cache_reads_heap": {
            "name": "virtual_read_cache.reads.heap"
        },
        "ocient_virtual_read_cache_total_blocks_disk": {
            "name": "virtual_read_cache.total_blocks.disk"
        },
        "ocient_vm_active_queries_count": {
            "name": "vm.active_queries_count"
        },
        "ocient_vm_datablock_router_network_rate": {
            "name": "vm.datablock_router.network_rate"
        },
        "ocient_vm_datablock_router_block_count": {
            "name": "vm.datablock_router.block_count"
        },
        "ocient_vm_datablock_router_budget": {
            "name": "vm.datablock_router.budget"
        },
        "ocient_vm_datablock_router_byte_count": {
            "name": "vm.datablock_router.byte_count"
        },
        "ocient_vm_fetchingCachedQueriesCount": {
            "name": "vm.fetchingCachedQueriesCount"
        },
        "ocient_vm_huge_block_alloc_count": {
            "name": "vm.huge_block.alloc_count"
        },
        "ocient_vm_huge_block_resizes": {
            "name": "vm.huge_block.resizes"
        },
        "ocient_vm_huge_memory_pool_allocated": {
            "name": "vm.huge_memory_pool.allocated"
        },
        "ocient_vm_long_dispatch_events": {
            "name": "vm.long_dispatch_events"
        },
        "ocient_vm_query_tree_probe_count": {
            "name": "vm.query_tree_probe.count"
        },
        "ocient_vm_queryTreeProbe_timeMs": {
            "name": "vm.queryTreeProbe.timeMs"
        },
        "ocient_vm_scheduler_no_work_oom_cycles": {
            "name": "vm.scheduler.no_work_oom_cycles"
        },
        "ocient_vm_scheduler_oom_killed_queries": {
            "name": "vm.scheduler.oom_killed_queries"
        },
        "ocient_vm_scheduler_opInstRuntimeRatio": {
            "name": "vm.scheduler.opInstRuntimeRatio"
        },
        "ocient_vm_stats_pdf_cache_size": {
            "name": "vm.stats.pdf_cache_size"
        },
        "ocient_vmprotocol_ping_countOver100ms": {
            "name": "vmprotocol.ping.countOver100ms"
        },
        "ocient_vmprotocol_ping_current": {
            "name": "vmprotocol.ping.current"
        }
    }
]