import os

from datadog_checks.dev import get_docker_hostname

HOST = get_docker_hostname()
PORT = 9644

INSTANCE_PORT = 9644
INSTANCE_URL = "http://{}:{}/public_metrics".format(HOST, INSTANCE_PORT)


REDPANDA_VERSION = os.getenv('REDPANDA_VERSION')

MOCK_REDPANDA_INSTANCE = {'openmetrics_endpoint': INSTANCE_URL, 'tags': ['instance_test']}

CHECK_NAME = 'redpanda'

INSTANCE_METRIC_GROUP_MAP = {
    'redpanda.application': [
        'redpanda.application.uptime',
        'redpanda.application.build',
        'redpanda.application.fips_mode',
    ],
    'redpanda.controller': [
        'redpanda.cluster.controller_log_limit_requests_available',
        'redpanda.cluster.controller_log_limit_requests_dropped.count',
    ],
    'redpanda.cloud': [
        'redpanda.cloud.client_backoff.count',
        'redpanda.cloud.client_pool_utilization',
        'redpanda.cloud.client_download_backoff.count',
        'redpanda.cloud.client_downloads.count',
        'redpanda.cloud.client_not_found.count',
        'redpanda.cloud.client_num_borrows.count',
        'redpanda.cloud.client_upload_backoff.count',
        'redpanda.cloud.client_uploads.count',
        'redpanda.cloud.storage.active_segments',
        'redpanda.cloud.storage.cache_op_hit.count',
        'redpanda.cloud.storage.op_in_progress_files',
        'redpanda.cloud.storage.cache_op_miss.count',
        'redpanda.cloud.storage.op_put.count',
        'redpanda.cloud.storage.cache_space_files',
        'redpanda.cloud.storage.cache_space_hwm_files',
        'redpanda.cloud.storage.cache_space_hwm_size_bytes',
        'redpanda.cloud.storage.cache_space_size_bytes',
        'redpanda.cloud.storage.cache_space_tracker_size',
        'redpanda.cloud.storage.cache_space_tracker_syncs.count',
        'redpanda.cloud.storage_cache_trim_carryover_trims.count',
        'redpanda.cloud.storage_cache_trim_exhaustive_trims.count',
        'redpanda.cloud.storage_cache_trim_failed_trims.count',
        'redpanda.cloud.storage_cache_trim_fast_trims.count',
        'redpanda.cloud.storage_cache_trim_in_mem_trims.count',
        'redpanda.cloud.storage_cloud_log_size',
        'redpanda.cloud.storage.deleted_segments.count',
        'redpanda.cloud.storage.errors.count',
        'redpanda.cloud.storage.housekeeping.drains',
        'redpanda.cloud.storage.housekeeping.jobs_completed.count',
        'redpanda.cloud.storage.housekeeping.jobs_failed.count',
        'redpanda.cloud.storage.housekeeping.jobs_skipped.count',
        'redpanda.cloud.storage.housekeeping.pauses',
        'redpanda.cloud.storage.housekeeping.resumes',
        'redpanda.cloud.storage_housekeeping_requests_throttled_average_rate',
        'redpanda.cloud.storage.housekeeping.rounds.count',
        'redpanda.cloud.storage.jobs.cloud_segment_reuploads',
        'redpanda.cloud.storage.jobs.local_segment_reuploads',
        'redpanda.cloud.storage.jobs.manifest_reuploads',
        'redpanda.cloud.storage.jobs.metadata_syncs',
        'redpanda.cloud.storage.jobs.segment_deletions',
        'redpanda.cloud.storage_limits_downloads_throttled_sum.count',
        'redpanda.cloud.storage_partition_manifest_uploads.count',
        'redpanda.cloud.storage_partition_readers',
        'redpanda.cloud.storage_partition_readers_delayed.count',
        'redpanda.cloud.storage_paused_archivers',
        'redpanda.cloud.storage.readers',
        'redpanda.cloud.storage_segment_index_uploads.count',
        'redpanda.cloud.storage_segment_materializations_delayed.count',
        'redpanda.cloud.storage_segment_readers_delayed.count',
        'redpanda.cloud.storage_segment_uploads.count',
        'redpanda.cloud.storage.segments',
        'redpanda.cloud.storage.segments_pending_deletion',
        'redpanda.cloud.storage_spillover_manifest_uploads.count',
        'redpanda.cloud.storage_spillover_manifests_materialized_bytes',
        'redpanda.cloud.storage_spillover_manifests_materialized_count',
        'redpanda.cloud.storage.uploaded_bytes.count',
    ],
    'redpanda.cluster': [
        'redpanda.cluster.brokers',
        'redpanda.cluster.features_enterprise_license_expiry_sec',
        'redpanda.cluster.latest_cluster_metadata_manifest_age',
        'redpanda.cluster.members_backend_queued_node_operations',
        'redpanda.cluster.non_homogenous_fips_mode',
        'redpanda.cluster.partition_num_with_broken_rack_constraint',
        'redpanda.cluster.partition_schema_id_validation_records_failed.count',
        'redpanda.cluster.partitions',
        'redpanda.cluster.topics',
        'redpanda.cluster.unavailable_partitions',
    ],
    'redpanda.debug_bundle': [
        'redpanda.debug_bundle.failed_generation_count.count',
        'redpanda.debug_bundle.last_failed_bundle_timestamp_seconds',
        'redpanda.debug_bundle.last_successful_bundle_timestamp_seconds',
        'redpanda.debug_bundle.successful_generation_count.count',
    ],
    'redpanda.rpc': [
        'redpanda.rpc.active_connections',
        'redpanda.rpc.received_bytes.count',
        'redpanda.rpc.request_errors.count',
        'redpanda.rpc.sent_bytes.count',
    ],
    'redpanda.io_queue': [
        'redpanda.io_queue.total_read_ops.count',
        'redpanda.io_queue.total_write_ops.count',
    ],
    'redpanda.kafka': [
        'redpanda.kafka.partition_committed_offset',
        'redpanda.kafka.partitions',
        'redpanda.kafka.records_fetched.count',
        'redpanda.kafka.records_produced.count',
        'redpanda.kafka.replicas',
        'redpanda.kafka.request_bytes.count',
        'redpanda.kafka.rpc_sasl_session_expiration.count',
        'redpanda.kafka.rpc_sasl_session_reauth_attempts.count',
        'redpanda.kafka.rpc_sasl_session_revoked.count',
        'redpanda.kafka.under_replicated_replicas',
    ],
    'redpanda.kafka.consumer_group_info': [
        'redpanda.kafka.group_count',
        'redpanda.kafka.group_topic_count',
    ],
    'redpanda.kafka.consumer_group_offset': [
        'redpanda.kafka.group_offset',
    ],
    'redpanda.kafka.consumer_group_lag': [
        'redpanda.kafka.group_lag_sum',
        'redpanda.kafka.group_lag_max',
    ],
    'redpanda.memory': [
        'redpanda.memory.allocated_memory',
        'redpanda.memory.available_memory',
        'redpanda.memory.available_memory_low_water_mark',
        'redpanda.memory.free_memory',
    ],
    'redpanda.node_status': [
        'redpanda.node_status.rpcs_received',
        'redpanda.node_status.rpcs_sent',
        'redpanda.node_status.rpcs_timed_out',
    ],
    'redpanda.pandaproxy': [
        'redpanda.pandaproxy.inflight_requests_memory_usage_ratio',
        'redpanda.pandaproxy.inflight_requests_usage_ratio',
        'redpanda.pandaproxy.queued_requests_memory_blocked',
        'redpanda.pandaproxy.request_errors.count',
    ],
    'redpanda.partitions': [
        'redpanda.partitions.moving_from_node',
        'redpanda.partitions.moving_to_node',
        'redpanda.partitions.node_cancelling_movements',
    ],
    'redpanda.raft': [
        'redpanda.raft.leadership_changes.count',
        'redpanda.raft.learners_gap_bytes',
        'redpanda.raft.recovery_offsets_pending',
        'redpanda.raft.recovery_bandwidth',
        'redpanda.raft.recovery_consumed_bandwidth',
        'redpanda.raft.recovery_partitions_active',
        'redpanda.raft.recovery_partitions_to_recover',
    ],
    'redpanda.reactor': [
        'redpanda.reactor.cpu_busy_seconds',
    ],
    'redpanda.scheduler': [
        'redpanda.scheduler.runtime_seconds.count',
    ],
    'redpanda.schemaregistry': [
        'redpanda.schema_registry.cache_schema_count',
        'redpanda.schema_registry.cache_schema_memory_bytes',
        'redpanda.schema_registry.cache_subject_count',
        'redpanda.schema_registry.cache_subject_version_count',
        'redpanda.schema_registry.inflight_requests_memory_usage_ratio',
        'redpanda.schema_registry.inflight_requests_usage_ratio',
        'redpanda.schema_registry.queued_requests_memory_blocked',
        'redpanda.schema_registry.errors.count',
    ],
    'redpanda.storage': [
        'redpanda.storage.cache_disk_free_bytes',
        'redpanda.storage.cache_disk_free_space_alert',
        'redpanda.storage.cache_disk_total_bytes',
        'redpanda.storage.disk_free_bytes',
        'redpanda.storage.disk_free_space_alert',
        'redpanda.storage.disk_total_bytes',
    ],
    'redpanda.iceberg': [
        'redpanda.iceberg.rest_client_active_gets',
        'redpanda.iceberg.rest_client_active_puts',
        'redpanda.iceberg.rest_client_active_requests',
        'redpanda.iceberg.rest_client_num_commit_table_update_requests.count',
        'redpanda.iceberg.rest_client_num_commit_table_update_requests_failed.count',
        'redpanda.iceberg.rest_client_num_create_namespace_requests.count',
        'redpanda.iceberg.rest_client_num_create_namespace_requests_failed.count',
        'redpanda.iceberg.rest_client_num_create_table_requests.count',
        'redpanda.iceberg.rest_client_num_create_table_requests_failed.count',
        'redpanda.iceberg.rest_client_num_drop_table_requests.count',
        'redpanda.iceberg.rest_client_num_drop_table_requests_failed.count',
        'redpanda.iceberg.rest_client_num_get_config_requests.count',
        'redpanda.iceberg.rest_client_num_get_config_requests_failed.count',
        'redpanda.iceberg.rest_client_num_load_table_requests.count',
        'redpanda.iceberg.rest_client_num_load_table_requests_failed.count',
        'redpanda.iceberg.rest_client_num_oauth_token_requests.count',
        'redpanda.iceberg.rest_client_num_oauth_token_requests_failed.count',
        'redpanda.iceberg.rest_client_num_request_timeouts.count',
        'redpanda.iceberg.rest_client_num_transport_errors.count',
        'redpanda.iceberg.rest_client_total_gets.count',
        'redpanda.iceberg.rest_client_total_inbound_bytes.count',
        'redpanda.iceberg.rest_client_total_outbound_bytes.count',
        'redpanda.iceberg.rest_client_total_puts.count',
        'redpanda.iceberg.rest_client_total_requests.count',
        'redpanda.iceberg.translation_decompressed_bytes_processed.count',
        'redpanda.iceberg.translation_dlq_files_created.count',
        'redpanda.iceberg.translation_files_created.count',
        'redpanda.iceberg.translation_invalid_records.count',
        'redpanda.iceberg.translation_parquet_bytes_added.count',
        'redpanda.iceberg.translation_parquet_rows_added.count',
        'redpanda.iceberg.translation_raw_bytes_processed.count',
        'redpanda.iceberg.translation_translations_finished.count',
    ],
    'redpanda.transform': [
        'redpanda.transform.execution_errors.count',
        'redpanda.transform.failures.count',
        'redpanda.transform.processor_lag.count',
        'redpanda.transform.read_bytes.count',
        'redpanda.transform.state',
        'redpanda.transform.write_bytes.count',
    ],
    'redpanda.wasm': [
        'redpanda.wasm.binary_executable_memory_usage',
        'redpanda.wasm.engine_cpu_seconds.count',
        'redpanda.wasm.engine_max_memory',
        'redpanda.wasm.engine_memory_usage',
    ],
    'redpanda.tls': [
        'redpanda.tls.certificate_expires_at_timestamp_seconds',
        'redpanda.tls.certificate_serial',
        'redpanda.tls.certificate_valid',
        'redpanda.tls.loaded_at_timestamp_seconds',
        'redpanda.tls.truststore_expires_at_timestamp_seconds',
    ],
    'redpanda.authorization': [
        'redpanda.authorization.result.count',
    ],
    'redpanda.security': [
        'redpanda.security.audit_errors.count',
        'redpanda.security.audit_last_event_timestamp_seconds.count',
    ],
}
# fmt: on

INSTANCE_HISTOGRAM_GROUP_MAP = {
    'redpanda.application': [],
    'redpanda.authorization': [],
    'redpanda.cloud': [
        'redpanda.cloud.client_lease_duration',
    ],
    'redpanda.cluster': [],
    'redpanda.controller': [],
    'redpanda.debug_bundle': [],
    'redpanda.iceberg': [],
    'redpanda.io_queue': [],
    'redpanda.kafka': [
        'redpanda.kafka.handler_latency_seconds',
        'redpanda.kafka.quotas_client_quota_throttle_time',
        'redpanda.kafka.quotas_client_quota_throughput',
        'redpanda.kafka.request_latency_seconds',
    ],
    'redpanda.kafka.consumer_group_info': [],
    'redpanda.kafka.consumer_group_lag': [],
    'redpanda.kafka.consumer_group_offset': [],
    'redpanda.memory': [],
    'redpanda.node_status': [],
    'redpanda.pandaproxy': [
        'redpanda.pandaproxy.request_latency',
    ],
    'redpanda.partitions': [],
    'redpanda.raft': [],
    'redpanda.reactor': [],
    'redpanda.rpc': [
        'redpanda.rpc.request_latency_seconds',
    ],
    'redpanda.scheduler': [],
    'redpanda.schemaregistry': [
        'redpanda.schema_registry.latency_seconds',
    ],
    'redpanda.security': [],
    'redpanda.storage': [],
    'redpanda.tls': [],
    'redpanda.transform': [
        'redpanda.transform.execution_latency_sec',
    ],
    'redpanda.wasm': [],
}

INSTANCE_DEFAULT_GROUPS = [
    'redpanda.application',
    'redpanda.authorization',
    'redpanda.cluster',
    'redpanda.io_queue',
    'redpanda.kafka',
    'redpanda.kafka.consumer_group_info',
    'redpanda.kafka.consumer_group_offset',
    'redpanda.kafka.consumer_group_lag',
    'redpanda.memory',
    'redpanda.partitions',
    'redpanda.raft',
    'redpanda.reactor',
    'redpanda.rpc',
    'redpanda.security',
    'redpanda.storage',
    'redpanda.tls',
]

INSTANCE_ADDITIONAL_GROUPS = [
    'redpanda.cloud',
    'redpanda.controller',
    'redpanda.debug_bundle',
    'redpanda.node_status',
    'redpanda.pandaproxy',
    'redpanda.scheduler',
    'redpanda.schemaregistry',
    'redpanda.iceberg',
    'redpanda.transform',
    'redpanda.wasm',
]


def get_metrics(metric_groups, group_map):
    """Given a list of metric groups, return single consolidated list"""
    return sorted(m for g in metric_groups for m in group_map[g])


INSTANCE_DEFAULT_METRICS = get_metrics(INSTANCE_DEFAULT_GROUPS, INSTANCE_METRIC_GROUP_MAP)
INSTANCE_DEFAULT_HISTOGRAMS = get_metrics(INSTANCE_DEFAULT_GROUPS, INSTANCE_HISTOGRAM_GROUP_MAP)
INSTANCE_ADDITIONAL_METRICS = get_metrics(INSTANCE_ADDITIONAL_GROUPS, INSTANCE_METRIC_GROUP_MAP)
INSTANCE_ADDITIONAL_HISTOGRAMS = get_metrics(INSTANCE_ADDITIONAL_GROUPS, INSTANCE_HISTOGRAM_GROUP_MAP)
