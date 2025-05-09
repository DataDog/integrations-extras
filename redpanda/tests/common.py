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
    ],
    'redpanda.controller': [
        'redpanda.controller.log_limit_requests_available',
        'redpanda.controller.log_limit_requests_dropped.count',
    ],
    'redpanda.cloud': [
        'redpanda.cloud.client_backoff.count',
        'redpanda.cloud.client_download_backoff.count',
        'redpanda.cloud.client_downloads.count',
        'redpanda.cloud.client_not_found.count',
        'redpanda.cloud.client_upload_backoff.count',
        'redpanda.cloud.client_uploads.count',
        'redpanda.cloud.storage.active_segments',
        'redpanda.cloud.storage.cache_op_hit.count',
        'redpanda.cloud.storage.op_in_progress_files',
        'redpanda.cloud.storage.cache_op_miss.count',
        'redpanda.cloud.storage.op_put.count',
        'redpanda.cloud.storage.cache_space_files',
        'redpanda.cloud.storage.cache_space_size_bytes',
        'redpanda.cloud.storage.deleted_segments.count',
        'redpanda.cloud.storage.errors.count',
        'redpanda.cloud.storage.housekeeping.drains',
        'redpanda.cloud.storage.housekeeping.jobs_completed.count',
        'redpanda.cloud.storage.housekeeping.jobs_failed.count',
        'redpanda.cloud.storage.housekeeping.jobs_skipped.count',
        'redpanda.cloud.storage.housekeeping.pauses',
        'redpanda.cloud.storage.housekeeping.resumes',
        'redpanda.cloud.storage.housekeeping.rounds.count',
        'redpanda.cloud.storage.jobs.cloud_segment_reuploads',
        'redpanda.cloud.storage.jobs.local_segment_reuploads',
        'redpanda.cloud.storage.jobs.manifest_reuploads',
        'redpanda.cloud.storage.jobs.metadata_syncs',
        'redpanda.cloud.storage.jobs.segment_deletions',
        'redpanda.cloud.storage.readers',
        'redpanda.cloud.storage.segments',
        'redpanda.cloud.storage.segments_pending_deletion',
        'redpanda.cloud.storage.uploaded_bytes.count',
    ],
    'redpanda.cluster': [
        'redpanda.cluster.brokers',
        'redpanda.cluster.partition_num_with_broken_rack_constraint',
        'redpanda.cluster.partitions',
        'redpanda.cluster.topics',
        'redpanda.cluster.unavailable_partitions',
    ],
    'redpanda.rpc': [
        'redpanda.rpc.active_connections',
        'redpanda.rpc.request_errors.count',
        'redpanda.rpc.request_latency_seconds.count',
        'redpanda.rpc.request_latency_seconds.bucket',
        'redpanda.rpc.request_latency_seconds.sum',
    ],
    'redpanda.io_queue': [
        'redpanda.io_queue.total_read_ops.count',
        'redpanda.io_queue.total_write_ops.count',
    ],
    'redpanda.kafka': [
        'redpanda.kafka.request_latency_seconds.sum',
        'redpanda.kafka.request_latency_seconds.bucket',
        'redpanda.kafka.request_latency_seconds.count',
        'redpanda.kafka.request_bytes.count',
        'redpanda.kafka.under_replicated_replicas',
        'redpanda.kafka.partition_committed_offset',
        'redpanda.kafka.partitions',
        'redpanda.kafka.replicas',
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
        'redpanda.pandaproxy.request_latency.count',
        'redpanda.pandaproxy.request_errors.count',
        'redpanda.pandaproxy.request_latency.bucket',
        'redpanda.pandaproxy.request_latency.sum',
    ],
    'redpanda.partitions': [
        'redpanda.partitions.moving_from_node',
        'redpanda.partitions.moving_to_node',
        'redpanda.partitions.node_cancelling_movements',
    ],
    'redpanda.raft': [
        'redpanda.raft.leadership_changes.count',
        'redpanda.raft.recovery_bandwidth',
    ],
    'redpanda.reactor': [
        'redpanda.reactor.cpu_busy_seconds',
    ],
    'redpanda.scheduler': [
        'redpanda.scheduler.runtime_seconds.count',
    ],
    'redpanda.schemaregistry': [
        'redpanda.schema_registry.errors.count',
        'redpanda.schema_registry_latency_seconds.count',
        'redpanda.schema_registry_latency_seconds.bucket',
        'redpanda.schema_registry_latency_seconds.sum',
    ],
    'redpanda.storage': [
        'redpanda.storage.disk_free_bytes',
        'redpanda.storage.disk_free_space_alert',
        'redpanda.storage.disk_total_bytes',
    ],
}
# fmt: on

INSTANCE_DEFAULT_GROUPS = [
    'redpanda.application',
    'redpanda.cluster',
    'redpanda.io_queue',
    'redpanda.kafka',
    'redpanda.kafka.consumer_group_info',
    'redpanda.kafka.consumer_group_lag',
    'redpanda.memory',
    'redpanda.partitions',
    'redpanda.raft',
    'redpanda.reactor',
    'redpanda.rpc',
    'redpanda.storage',
]

INSTANCE_ADDITIONAL_GROUPS = [
    'redpanda.cloud',
    'redpanda.controller',
    'redpanda.kafka.consumer_group_offset',
    'redpanda.node_status',
    'redpanda.pandaproxy',
    'redpanda.scheduler',
    'redpanda.schemaregistry',
]


def get_metrics(metric_groups):
    """Given a list of metric groups, return single consolidated list"""
    return sorted(m for g in metric_groups for m in INSTANCE_METRIC_GROUP_MAP[g])


INSTANCE_DEFAULT_METRICS = get_metrics(INSTANCE_DEFAULT_GROUPS)
INSTANCE_ADDITIONAL_METRICS = get_metrics(INSTANCE_ADDITIONAL_GROUPS)
