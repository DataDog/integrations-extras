# metrics namespaced under 'redpanda'
REDPANDA_APPLICATION = {
    'redpanda_application_uptime_seconds_total': 'application.uptime',
    'redpanda_application_build': 'application.build',
    'redpanda_application_fips_mode': 'application.fips_mode'
}

REDPANDA_CONTROLLER = {
    'redpanda_cluster_controller_log_limit_requests_available_rps': 'controller.log_limit_requests_available',
    'redpanda_cluster_controller_log_limit_requests_dropped': 'controller.log_limit_requests_dropped',
}

REDPANDA_CLOUD = {
    'redpanda_cloud_client_backoff': 'cloud.client_backoff',
    'redpanda_cloud_client_client_pool_utilization': 'cloud.client_pool_utilization',
    'redpanda_cloud_client_download_backoff': 'cloud.client_download_backoff',
    'redpanda_cloud_client_downloads': 'cloud.client_downloads',
    'redpanda_cloud_client_lease_duration': 'cloud.client_lease_duration',
    'redpanda_cloud_client_not_found': 'cloud.client_not_found',
    'redpanda_cloud_client_num_borrows': 'cloud.client_num_borrows',
    'redpanda_cloud_client_upload_backoff': 'cloud.client_upload_backoff',
    'redpanda_cloud_client_uploads': 'cloud.client_uploads',
    'redpanda_cloud_storage_active_segments': 'cloud.storage.active_segments',
    'redpanda_cloud_storage_cache_op_hit': 'cloud.storage.cache_op_hit',
    'redpanda_cloud_storage_cache_op_in_progress_files': 'cloud.storage.op_in_progress_files',
    'redpanda_cloud_storage_cache_op_miss': 'cloud.storage.cache_op_miss',
    'redpanda_cloud_storage_cache_op_put': 'cloud.storage.op_put',
    'redpanda_cloud_storage_cache_space_files': 'cloud.storage.cache_space_files',
    'redpanda_cloud_storage_cache_space_hwm_files': 'cloud.storage.cache_space_hwm_files',
    'redpanda_cloud_storage_cache_space_hwm_size_bytes': 'cloud.storage.cache_space_hwm_size_bytes',
    'redpanda_cloud_storage_cache_space_size_bytes': 'cloud.storage.cache_space_size_bytes',
    'redpanda_cloud_storage_cache_space_tracker_size': 'cloud.storage.cache_space_tracker_size',
    'redpanda_cloud_storage_cache_space_tracker_syncs': 'cloud.storage.cache_space_tracker_syncs',
    'redpanda_cloud_storage_cache_trim_carryover_trims': 'cloud.storage_cache_trim_carryover_trims',
    'redpanda_cloud_storage_cache_trim_exhaustive_trims': 'cloud.storage_cache_trim_exhaustive_trims',
    'redpanda_cloud_storage_cache_trim_failed_trims': 'cloud.storage_cache_trim_failed_trims',
    'redpanda_cloud_storage_cache_trim_fast_trims': 'cloud.storage_cache_trim_fast_trims',
    'redpanda_cloud_storage_cache_trim_in_mem_trims': 'cloud.storage_cache_trim_in_mem_trims',
    'redpanda_cloud_storage_cloud_log_size': 'cloud.storage_cloud_log_size',
    'redpanda_cloud_storage_deleted_segments': 'cloud.storage.deleted_segments',
    'redpanda_cloud_storage_errors': 'cloud.storage.errors',
    'redpanda_cloud_storage_housekeeping_drains': 'cloud.storage.housekeeping.drains',
    'redpanda_cloud_storage_housekeeping_jobs_completed': 'cloud.storage.housekeeping.jobs_completed',
    'redpanda_cloud_storage_housekeeping_jobs_failed': 'cloud.storage.housekeeping.jobs_failed',
    'redpanda_cloud_storage_housekeeping_jobs_skipped': 'cloud.storage.housekeeping.jobs_skipped',
    'redpanda_cloud_storage_housekeeping_pauses': 'cloud.storage.housekeeping.pauses',
    'redpanda_cloud_storage_housekeeping_resumes': 'cloud.storage.housekeeping.resumes',
    'redpanda_cloud_storage_housekeeping_requests_throttled_average_rate': 'cloud.storage_housekeeping_requests_throttled_average_rate',
    'redpanda_cloud_storage_housekeeping_rounds': 'cloud.storage.housekeeping.rounds',
    'redpanda_cloud_storage_jobs_cloud_segment_reuploads': 'cloud.storage.jobs.cloud_segment_reuploads',
    'redpanda_cloud_storage_jobs_local_segment_reuploads': 'cloud.storage.jobs.local_segment_reuploads',
    'redpanda_cloud_storage_jobs_manifest_reuploads': 'cloud.storage.jobs.manifest_reuploads',
    'redpanda_cloud_storage_jobs_metadata_syncs': 'cloud.storage.jobs.metadata_syncs',
    'redpanda_cloud_storage_jobs_segment_deletions': 'cloud.storage.jobs.segment_deletions',
    'redpanda_cloud_storage_limits_downloads_throttled_sum': 'cloud.storage_limits_downloads_throttled_sum',
    'redpanda_cloud_storage_partition_manifest_uploads': 'cloud.storage_partition_manifest_uploads',
    'redpanda_cloud_storage_partition_readers': 'cloud.storage_partition_readers',
    'redpanda_cloud_storage_partition_readers_delayed': 'cloud.storage_partition_readers_delayed',
    'redpanda_cloud_storage_paused_archivers': 'cloud.storage_paused_archivers',
    'redpanda_cloud_storage_readers': 'cloud.storage.readers',
    'redpanda_cloud_storage_segment_index_uploads': 'cloud.storage_segment_index_uploads',
    'redpanda_cloud_storage_segment_materializations_delayed': 'cloud.storage_segment_materializations_delayed',
    'redpanda_cloud_storage_segment_readers_delayed': 'cloud.storage_segment_readers_delayed',
    'redpanda_cloud_storage_segment_uploads': 'cloud.storage_segment_uploads',
    'redpanda_cloud_storage_segments': 'cloud.storage.segments',
    'redpanda_cloud_storage_segments_pending_deletion': 'cloud.storage.segments_pending_deletion',
    'redpanda_cloud_storage_spillover_manifest_uploads': 'cloud.storage_spillover_manifest_uploads',
    'redpanda_cloud_storage_spillover_manifests_materialized_bytes': 'cloud.storage_spillover_manifests_materialized_bytes',
    'redpanda_cloud_storage_spillover_manifests_materialized_count': 'cloud.storage_spillover_manifests_materialized_count',
    'redpanda_cloud_storage_uploaded_bytes': 'cloud.storage.uploaded_bytes',
}

REDPANDA_CLUSTER = {
    'redpanda_cluster_brokers': 'cluster.brokers',
    'redpanda_cluster_features_enterprise_license_expiry_sec': 'cluster.features_enterprise_license_expiry_sec',
    'redpanda_cluster_latest_cluster_metadata_manifest_age': 'cluster.latest_cluster_metadata_manifest_age',
    'redpanda_cluster_members_backend_queued_node_operations': 'cluster.members_backend_queued_node_operations',
    'redpanda_cluster_non_homogenous_fips_mode': 'cluster.non_homogenous_fips_mode',
    'redpanda_cluster_partition_num_with_broken_rack_constraint': 'cluster.partition_num_with_broken_rack_constraint',
    'redpanda_cluster_partition_schema_id_validation_records_failed': 'cluster.partition_schema_id_validation_records_failed',
    'redpanda_cluster_partitions': 'cluster.partitions',
    'redpanda_cluster_topics': 'cluster.topics',
    'redpanda_cluster_unavailable_partitions': 'cluster.unavailable_partitions',
}

REDPANDA_DEBUG_BUNDLE = {
    'redpanda_debug_bundle_failed_generation_count': 'debug_bundle.failed_generation_count',
    'redpanda_debug_bundle_last_failed_bundle_timestamp_seconds': 'debug_bundle.last_failed_bundle_timestamp_seconds',
    'redpanda_debug_bundle_last_successful_bundle_timestamp_seconds': 'debug_bundle.last_successful_bundle_timestamp_seconds',
    'redpanda_debug_bundle_successful_generation_count': 'debug_bundle.successful_generation_count',
}

REDPANDA_RPC = {
    'redpanda_rpc_active_connections': 'rpc.active_connections',
    'redpanda_rpc_received_bytes': 'rpc.received_bytes',
    'redpanda_rpc_request_errors': 'rpc.request_errors',
    'redpanda_rpc_request_latency_seconds': 'rpc.request_latency_seconds',
    'redpanda_rpc_sent_bytes': 'rpc.sent_bytes',
}

REDPANDA_IO_QUEUE = {
    'redpanda_io_queue_total_read_ops': 'io_queue.total_read_ops',
    'redpanda_io_queue_total_write_ops': 'io_queue.total_write_ops',
}

REDPANDA_KAFKA = {
    'redpanda_kafka_handler_latency_seconds': 'kafka.handler_latency_seconds',
    'redpanda_kafka_max_offset': 'kafka.partition_committed_offset',
    'redpanda_kafka_partitions': 'kafka.partitions',
    'redpanda_kafka_quotas_client_quota_throttle_time': 'kafka.quotas_client_quota_throttle_time',
    'redpanda_kafka_quotas_client_quota_throughput': 'kafka.quotas_client_quota_throughput',
    'redpanda_kafka_records_fetched': 'kafka.records_fetched',
    'redpanda_kafka_records_produced': 'kafka.records_produced',
    'redpanda_kafka_replicas': 'kafka.replicas',
    'redpanda_kafka_request_latency_seconds': 'kafka.request_latency_seconds',
    'redpanda_kafka_request_bytes': 'kafka.request_bytes',
    'redpanda_kafka_rpc_sasl_session_expiration': 'kafka.rpc_sasl_session_expiration',
    'redpanda_kafka_rpc_sasl_session_reauth_attempts': 'kafka.rpc_sasl_session_reauth_attempts',
    'redpanda_kafka_rpc_sasl_session_revoked': 'kafka.rpc_sasl_session_revoked',
    'redpanda_kafka_under_replicated_replicas': 'kafka.under_replicated_replicas',
}

# As of Redpanda v25.1, can be disabled by removing "group"
# from cluster config "enable_consumer_group_metrics"
REDPANDA_KAFKA_CONSUMER_GROUP_INFO = {
    'redpanda_kafka_consumer_group_consumers': 'kafka.group_count',
    'redpanda_kafka_consumer_group_topics': 'kafka.group_topic_count',
}

# As of Redpanda v25.1, can be disabled by removing "partition"
# from cluster config "enable_consumer_group_metrics"
REDPANDA_KAFKA_CONSUMER_GROUP_OFFSET = {
    'redpanda_kafka_consumer_group_committed_offset': 'kafka.group_offset',
}

# As of Redpanda v25.1, can be enabled by adding "consumer_lag"
# to cluster config "enable_consumer_group_metrics"
REDPANDA_KAFKA_CONSUMER_GROUP_LAG = {
    'redpanda_kafka_consumer_group_lag_sum': 'kafka.group_lag_sum',
    'redpanda_kafka_consumer_group_lag_max': 'kafka.group_lag_max',
}

REDPANDA_MEMORY = {
    'redpanda_memory_allocated_memory': 'memory.allocated_memory',
    'redpanda_memory_available_memory': 'memory.available_memory',
    'redpanda_memory_available_memory_low_water_mark': 'memory.available_memory_low_water_mark',
    'redpanda_memory_free_memory': 'memory.free_memory',
}

REDPANDA_NODE_STATUS_RPC = {
    'redpanda_node_status_rpcs_received': 'node_status.rpcs_received',
    'redpanda_node_status_rpcs_sent': 'node_status.rpcs_sent',
    'redpanda_node_status_rpcs_timed_out': 'node_status.rpcs_timed_out',
}

REDPANDA_PANDAPROXY = {
    'redpanda_rest_proxy_inflight_requests_memory_usage_ratio': 'pandaproxy.inflight_requests_memory_usage_ratio',
    'redpanda_rest_proxy_inflight_requests_usage_ratio': 'pandaproxy.inflight_requests_usage_ratio',
    'redpanda_rest_proxy_queued_requests_memory_blocked': 'pandaproxy.queued_requests_memory_blocked',
    'redpanda_rest_proxy_request_latency_seconds': 'pandaproxy.request_latency',
    'redpanda_rest_proxy_request_errors': 'pandaproxy.request_errors',
}

REDPANDA_CLUSTER_PARTITION = {
    'redpanda_cluster_partition_moving_from_node': 'partitions.moving_from_node',
    'redpanda_cluster_partition_moving_to_node': 'partitions.moving_to_node',
    'redpanda_cluster_partition_node_cancelling_movements': 'partitions.node_cancelling_movements',
}

REDPANDA_RAFT = {
    'redpanda_raft_leadership_changes': 'raft.leadership_changes',
    'redpanda_raft_learners_gap_bytes': 'raft.learners_gap_bytes',
    'redpanda_raft_recovery_offsets_pending': 'raft.recovery_offsets_pending',
    'redpanda_raft_recovery_partition_movement_available_bandwidth': 'raft.recovery_bandwidth',
    'redpanda_raft_recovery_partition_movement_consumed_bandwidth': 'raft.recovery_consumed_bandwidth',
    'redpanda_raft_recovery_partitions_active': 'raft.recovery_partitions_active',
    'redpanda_raft_recovery_partitions_to_recover': 'raft.recovery_partitions_to_recover',
}

REDPANDA_REACTOR = {
    'redpanda_cpu_busy_seconds_total': 'reactor.cpu_busy_seconds',
}

REDPANDA_SCHEDULER = {
    'redpanda_scheduler_runtime_seconds': 'scheduler.runtime_seconds',
}

REDPANDA_SCHEMA_REGISTRY = {
    'redpanda_schema_registry_cache_schema_count': 'schema_registry.cache_schema_count',
    'redpanda_schema_registry_cache_schema_memory_bytes': 'schema_registry.cache_schema_memory_bytes',
    'redpanda_schema_registry_cache_subject_count': 'schema_registry.cache_subject_count',
    'redpanda_schema_registry_cache_subject_version_count': 'schema_registry.cache_subject_version_count',
    'redpanda_schema_registry_inflight_requests_memory_usage_ratio': 'schema_registry.inflight_requests_memory_usage_ratio',
    'redpanda_schema_registry_inflight_requests_usage_ratio': 'schema_registry.inflight_requests_usage_ratio',
    'redpanda_schema_registry_queued_requests_memory_blocked': 'schema_registry.queued_requests_memory_blocked',
    'redpanda_schema_registry_request_errors': 'schema_registry.errors',
    'redpanda_schema_registry_request_latency_seconds': 'schema_registry.latency_seconds',
}

REDPANDA_STORAGE = {
    'redpanda_storage_cache_disk_free_bytes': 'storage.cache_disk_free_bytes',
    'redpanda_storage_cache_disk_free_space_alert': 'storage.cache_disk_free_space_alert',
    'redpanda_storage_disk_free_bytes': 'storage.disk_free_bytes',
    'redpanda_storage_disk_free_space_alert': 'storage.disk_free_space_alert',
    'redpanda_storage_disk_total_bytes': 'storage.disk_total_bytes',
}

REDPANDA_ICEBERG = {
    'redpanda_iceberg_rest_client_active_gets': 'iceberg.rest_client_active_gets',
    'redpanda_iceberg_rest_client_active_puts': 'iceberg.rest_client_active_puts',
    'redpanda_iceberg_rest_client_active_requests': 'iceberg.rest_client_active_requests',
    'redpanda_iceberg_rest_client_num_commit_table_update_requests': 'iceberg.rest_client_num_commit_table_update_requests',
    'redpanda_iceberg_rest_client_num_commit_table_update_requests_failed': 'iceberg.rest_client_num_commit_table_update_requests_failed',
    'redpanda_iceberg_rest_client_num_create_namespace_requests': 'iceberg.rest_client_num_create_namespace_requests',
    'redpanda_iceberg_rest_client_num_create_namespace_requests_failed': 'iceberg.rest_client_num_create_namespace_requests_failed',
    'redpanda_iceberg_rest_client_num_create_table_requests': 'iceberg.rest_client_num_create_table_requests',
    'redpanda_iceberg_rest_client_num_create_table_requests_failed': 'iceberg.rest_client_num_create_table_requests_failed',
    'redpanda_iceberg_rest_client_num_drop_table_requests': 'iceberg.rest_client_num_drop_table_requests',
    'redpanda_iceberg_rest_client_num_drop_table_requests_failed': 'iceberg.rest_client_num_drop_table_requests_failed',
    'redpanda_iceberg_rest_client_num_get_config_requests': 'iceberg.rest_client_num_get_config_requests',
    'redpanda_iceberg_rest_client_num_get_config_requests_failed': 'iceberg.rest_client_num_get_config_requests_failed',
    'redpanda_iceberg_rest_client_num_load_table_requests': 'iceberg.rest_client_num_load_table_requests',
    'redpanda_iceberg_rest_client_num_load_table_requests_failed': 'iceberg.rest_client_num_load_table_requests_failed',
    'redpanda_iceberg_rest_client_num_oauth_token_requests': 'iceberg.rest_client_num_oauth_token_requests',
    'redpanda_iceberg_rest_client_num_oauth_token_requests_failed': 'iceberg.rest_client_num_oauth_token_requests_failed',
    'redpanda_iceberg_rest_client_num_request_timeouts': 'iceberg.rest_client_num_request_timeouts',
    'redpanda_iceberg_rest_client_num_transport_errors': 'iceberg.rest_client_num_transport_errors',
    'redpanda_iceberg_rest_client_total_gets': 'iceberg.rest_client_total_gets',
    'redpanda_iceberg_rest_client_total_inbound_bytes': 'iceberg.rest_client_total_inbound_bytes',
    'redpanda_iceberg_rest_client_total_outbound_bytes': 'iceberg.rest_client_total_outbound_bytes',
    'redpanda_iceberg_rest_client_total_puts': 'iceberg.rest_client_total_puts',
    'redpanda_iceberg_rest_client_total_requests': 'iceberg.rest_client_total_requests',
    'redpanda_iceberg_translation_decompressed_bytes_processed': 'iceberg.translation_decompressed_bytes_processed',
    'redpanda_iceberg_translation_dlq_files_created': 'iceberg.translation_dlq_files_created',
    'redpanda_iceberg_translation_files_created': 'iceberg.translation_files_created',
    'redpanda_iceberg_translation_invalid_records': 'iceberg.translation_invalid_records',
    'redpanda_iceberg_translation_parquet_bytes_added': 'iceberg.translation_parquet_bytes_added',
    'redpanda_iceberg_translation_parquet_rows_added': 'iceberg.translation_parquet_rows_added',
    'redpanda_iceberg_translation_raw_bytes_processed': 'iceberg.translation_raw_bytes_processed',
    'redpanda_iceberg_translation_translations_finished': 'iceberg.translation_translations_finished',
}

REDPANDA_TRANSFORM = {
    'redpanda_transform_execution_errors': 'transform.execution_errors',
    'redpanda_transform_execution_latency_sec': 'transform.execution_latency_sec',
    'redpanda_transform_failures': 'transform.failures',
    'redpanda_transform_processor_lag': 'transform.processor_lag',
    'redpanda_transform_read_bytes': 'transform.read_bytes',
    'redpanda_transform_state': 'transform.state',
    'redpanda_transform_write_bytes': 'transform.write_bytes',
}

REDPANDA_WASM = {
    'redpanda_wasm_binary_executable_memory_usage': 'wasm.binary_executable_memory_usage',
    'redpanda_wasm_engine_cpu_seconds': 'wasm.engine_cpu_seconds',
    'redpanda_wasm_engine_max_memory': 'wasm.engine_max_memory',
    'redpanda_wasm_engine_memory_usage': 'wasm.engine_memory_usage',
}

REDPANDA_TLS = {
    'redpanda_tls_certificate_expires_at_timestamp_seconds': 'tls.certificate_expires_at_timestamp_seconds',
    'redpanda_tls_certificate_serial': 'tls.certificate_serial',
    'redpanda_tls_certificate_valid': 'tls.certificate_valid',
    'redpanda_tls_loaded_at_timestamp_seconds': 'tls.loaded_at_timestamp_seconds',
    'redpanda_tls_truststore_expires_at_timestamp_seconds': 'tls.truststore_expires_at_timestamp_seconds',
}

REDPANDA_AUTHORIZATION = {
    'redpanda_authorization_result': 'authorization.result',
}

REDPANDA_SECURITY = {
    'redpanda_security_audit_errors': 'security.audit_errors',
    'redpanda_security_audit_last_event_timestamp_seconds': 'security.audit_last_event_timestamp_seconds',
}

INSTANCE_DEFAULT_METRICS = [
    REDPANDA_APPLICATION,
    REDPANDA_AUTHORIZATION,
    REDPANDA_CLUSTER,
    REDPANDA_CLUSTER_PARTITION,
    REDPANDA_IO_QUEUE,
    REDPANDA_KAFKA,
    REDPANDA_KAFKA_CONSUMER_GROUP_INFO,
    REDPANDA_KAFKA_CONSUMER_GROUP_OFFSET,
    REDPANDA_KAFKA_CONSUMER_GROUP_LAG,
    REDPANDA_MEMORY,
    REDPANDA_RAFT,
    REDPANDA_REACTOR,
    REDPANDA_RPC,
    REDPANDA_SECURITY,
    REDPANDA_STORAGE,
    REDPANDA_TLS,
]

ADDITIONAL_METRICS_MAP = {
    'redpanda.cloud': REDPANDA_CLOUD,
    'redpanda.controller': REDPANDA_CONTROLLER,
    'redpanda.debug_bundle': REDPANDA_DEBUG_BUNDLE,
    'redpanda.node_status': REDPANDA_NODE_STATUS_RPC,
    'redpanda.pandaproxy': REDPANDA_PANDAPROXY,
    'redpanda.scheduler': REDPANDA_SCHEDULER,
    'redpanda.schemaregistry': REDPANDA_SCHEMA_REGISTRY,
    'redpanda.iceberg': REDPANDA_ICEBERG,
    'redpanda.transform': REDPANDA_TRANSFORM,
    'redpanda.wasm': REDPANDA_WASM
}
