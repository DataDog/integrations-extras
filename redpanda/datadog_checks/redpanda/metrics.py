# metrics namespaced under 'redpanda'
REDPANDA_APPLICATION = {
    'redpanda_application_uptime_seconds_total': 'application.uptime',
    'redpanda_application_build': 'application.build',
}

REDPANDA_CONTROLLER = {
    'redpanda_cluster_controller_log_limit_requests_available_rps': 'controller.log_limit_requests_available',
    'redpanda_cluster_controller_log_limit_requests_dropped': 'controller.log_limit_requests_dropped',
}

REDPANDA_CLOUD = {
    'redpanda_cloud_client_backoff': 'cloud.client_backoff',
    'redpanda_cloud_client_dowload_backoff': 'cloud.client_download_backoff',
    'redpanda_cloud_client_downloads': 'cloud.client_downloads',
    'redpanda_cloud_client_not_found': 'cloud.client_not_found',
    'redpanda_cloud_client_upload_backoff': 'cloud.client_upload_backoff',
    'redpanda_cloud_client_uploads': 'cloud.client_uploads',
    'redpanda_cloud_storage_active_segments': 'cloud.storage.active_segments',
    'redpanda_cloud_storage_cache_op_hit': 'cloud.storage.cache_op_hit',
    'redpanda_cloud_storage_cache_op_in_progress_files': 'cloud.storage.op_in_progress_files',
    'redpanda_cloud_storage_cache_op_miss': 'cloud.storage.cache_op_miss',
    'redpanda_cloud_storage_cache_op_put': 'cloud.storage.op_put',
    'redpanda_cloud_storage_cache_space_files': 'cloud.storage.cache_space_files',
    'redpanda_cloud_storage_cache_space_size_bytes': 'cloud.storage.cache_space_size_bytes',
    'redpanda_cloud_storage_deleted_segments': 'cloud.storage.deleted_segments',
    'redpanda_cloud_storage_errors': 'cloud.storage.errors',
    'redpanda_cloud_storage_housekeeping_drains': 'cloud.storage.housekeeping.drains',
    'redpanda_cloud_storage_housekeeping_jobs_completed': 'cloud.storage.housekeeping.jobs_completed',
    'redpanda_cloud_storage_housekeeping_jobs_failed': 'cloud.storage.housekeeping.jobs_failed',
    'redpanda_cloud_storage_housekeeping_jobs_skipped': 'cloud.storage.housekeeping.jobs_skipped',
    'redpanda_cloud_storage_housekeeping_pauses': 'cloud.storage.housekeeping.pauses',
    'redpanda_cloud_storage_housekeeping_resumes': 'cloud.storage.housekeeping.resumes',
    'redpanda_cloud_storage_housekeeping_rounds': 'cloud.storage.housekeeping.rounds',
    'redpanda_cloud_storage_jobs_cloud_segment_reuploads': 'cloud.storage.jobs.cloud_segment_reuploads',
    'redpanda_cloud_storage_jobs_local_segment_reuploads': 'cloud.storage.jobs.local_segment_reuploads',
    'redpanda_cloud_storage_jobs_manifest_reuploads': 'cloud.storage.jobs.manifest_reuploads',
    'redpanda_cloud_storage_jobs_metadata_syncs': 'cloud.storage.jobs.metadata_syncs',
    'redpanda_cloud_storage_jobs_segment_deletions': 'cloud.storage.jobs.segment_deletions',
    'redpanda_cloud_storage_readers': 'cloud.storage.readers',
    'redpanda_cloud_storage_segments': 'cloud.storage.segments',
    'redpanda_cloud_storage_segments_pending_deletion': 'cloud.storage.segments_pending_deletion',
    'redpanda_cloud_storage_uploaded_bytes': 'cloud.storage.uploaded_bytes',
}

REDPANDA_CLUSTER = {
    'redpanda_cluster_brokers': 'cluster.brokers',
    'redpanda_cluster_partition_num_with_broken_rack_constraint': 'cluster.partition_num_with_broken_rack_constraint',
    'redpanda_cluster_partitions': 'cluster.partitions',
    'redpanda_cluster_topics': 'cluster.topics',
    'redpanda_cluster_unavailable_partitions': 'cluster.unavailable_partitions',
}

REDPANDA_RPC = {
    'redpanda_rpc_active_connections': 'rpc.active_connections',
    'redpanda_rpc_request_errors': 'rpc.request_errors',
    'redpanda_rpc_request_latency_seconds': 'rpc.request_latency_seconds',
}

REDPANDA_IO_QUEUE = {
    'redpanda_io_queue_total_read_ops': 'io_queue.total_read_ops',
    'redpanda_io_queue_total_write_ops': 'io_queue.total_write_ops',
}

REDPANDA_KAFKA = {
    'redpanda_kafka_max_offset': 'kafka.partition_committed_offset',
    'redpanda_kafka_partitions': 'kafka.partitions',
    'redpanda_kafka_replicas': 'kafka.replicas',
    'redpanda_kafka_request_latency_seconds': 'kafka.request_latency_seconds',
    'redpanda_kafka_request_bytes': 'kafka.request_bytes',
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
    'redpanda_raft_recovery_partition_movement_available_bandwidth': 'raft.recovery_bandwidth',
}

REDPANDA_REACTOR = {
    'redpanda_cpu_busy_seconds_total': 'reactor.cpu_busy_seconds',
}

REDPANDA_SCHEDULER = {
    'redpanda_scheduler_runtime_seconds': 'scheduler.runtime_seconds',
}

REDPANDA_SCHEMA_REGISTRY = {
    'redpanda_schema_registry_request_errors': 'schema_registry.errors',
    'redpanda_schema_registry_request_latency_seconds': 'schema_registry_latency_seconds',
}

REDPANDA_STORAGE = {
    'redpanda_storage_disk_free_bytes': 'storage.disk_free_bytes',
    'redpanda_storage_disk_free_space_alert': 'storage.disk_free_space_alert',
    'redpanda_storage_disk_total_bytes': 'storage.disk_total_bytes',
}

INSTANCE_DEFAULT_METRICS = [
    REDPANDA_APPLICATION,
    REDPANDA_CLUSTER,
    REDPANDA_CLUSTER_PARTITION,
    REDPANDA_IO_QUEUE,
    REDPANDA_KAFKA,
    REDPANDA_KAFKA_CONSUMER_GROUP_INFO,
    REDPANDA_KAFKA_CONSUMER_GROUP_OFFSET,
    REDPANDA_MEMORY,
    REDPANDA_RAFT,
    REDPANDA_REACTOR,
    REDPANDA_RPC,
    REDPANDA_STORAGE,
]

ADDITIONAL_METRICS_MAP = {
    'redpanda.cloud': REDPANDA_CLOUD,
    'redpanda.controller': REDPANDA_CONTROLLER,
    'redpanda.node_status': REDPANDA_NODE_STATUS_RPC,
    'redpanda.pandaproxy': REDPANDA_PANDAPROXY,
    'redpanda.scheduler': REDPANDA_SCHEDULER,
    'redpanda.schemaregistry': REDPANDA_SCHEMA_REGISTRY,
    'redpanda.kafka.consumer_group_lag': REDPANDA_KAFKA_CONSUMER_GROUP_LAG,
}
