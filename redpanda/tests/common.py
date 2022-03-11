import os

from datadog_checks.dev import get_docker_hostname

HOST = get_docker_hostname()
PORT = 9644

INSTANCE_PORT = 9644
INSTANCE_URL = "http://{}:{}/metrics".format(HOST, INSTANCE_PORT)


REDPANDA_VERSION = os.getenv('REDPANDA_VERSION')

MOCK_REDPANDA_INSTANCE = {'openmetrics_endpoint': INSTANCE_URL, 'tags': ['instance_test']}

CHECK_NAME = 'redpanda'

INSTANCE_METRIC_GROUP_MAP = {
    'redpanda.application': [
        'redpanda.application.uptime',
        'redpanda.application.build',
    ],
    'redpanda.alien': [
        'redpanda.alien.receive_batch_queue_length',
        'redpanda.alien.total_received_messages.count',
        'redpanda.alien.total_sent_messages.count',
    ],
    'redpanda.cluster': [
        'redpanda.cluster.partition_committed_offset',
        'redpanda.cluster.partition_end_offset',
        'redpanda.cluster.partition_high_watermark',
        'redpanda.cluster.partition_last_stable_offset',
        'redpanda.cluster.partition_leader',
        'redpanda.cluster.partition_leader_id',
        'redpanda.cluster.partition_records_fetched.count',
        'redpanda.cluster.partition_records_produced.count',
        'redpanda.cluster.partition_under_replicated_replicas',
    ],
    'redpanda.httpd': [
        'redpanda.httpd.connections_current',
        'redpanda.httpd.connections.count',
        'redpanda.httpd.read_errors.count',
        'redpanda.httpd.reply_errors.count',
        'redpanda.httpd.requests_served.count',
    ],
    'redpanda.internal_rpc': [
        'redpanda.internal_rpc.active_connections',
        'redpanda.internal_rpc.connection_close_errors.count',
        'redpanda.internal_rpc.connects.count',
        'redpanda.internal_rpc.consumed_mem_bytes.count',
        'redpanda.internal_rpc.corrupted_headers.count',
        'redpanda.internal_rpc.dispatch_handler_latency.sum',
        'redpanda.internal_rpc.dispatch_handler_latency.count',
        'redpanda.internal_rpc.dispatch_handler_latency.bucket',
        'redpanda.internal_rpc.max_service_mem_bytes.count',
        'redpanda.internal_rpc.method_not_found_errors.count',
        'redpanda.internal_rpc.received_bytes.count',
        'redpanda.internal_rpc.requests_blocked_memory.count',
        'redpanda.internal_rpc.requests_completed.count',
        'redpanda.internal_rpc.requests_pending',
        'redpanda.internal_rpc.sent_bytes.count',
        'redpanda.internal_rpc.service_errors.count',
    ],
    'redpanda.io_queue': [
        'redpanda.io_queue.delay',
        'redpanda.io_queue.queue_length',
        'redpanda.io_queue.shares',
        'redpanda.io_queue.total_bytes.count',
        'redpanda.io_queue.total_delay_sec.count',
        'redpanda.io_queue.total_operations.count',
    ],
    'redpanda.kafka': [
        'redpanda.kafka.fetch_sessions_cache_mem_usage_bytes',
        'redpanda.kafka.fetch_sessions_cache_sessions_count',
        'redpanda.kafka.latency_fetch_latency_us.sum',
        'redpanda.kafka.latency_fetch_latency_us.count',
        'redpanda.kafka.latency_fetch_latency_us.bucket',
        'redpanda.kafka.latency_produce_latency_us.sum',
        'redpanda.kafka.latency_produce_latency_us.count',
        'redpanda.kafka.latency_produce_latency_us.bucket',
        'redpanda.kafka.rpc_active_connections',
        'redpanda.kafka.rpc_connection_close_errors.count',
        'redpanda.kafka.rpc_connects.count',
        'redpanda.kafka.rpc_consumed_mem_bytes.count',
        'redpanda.kafka.rpc_corrupted_headers.count',
        'redpanda.kafka.rpc_dispatch_handler_latency.sum',
        'redpanda.kafka.rpc_dispatch_handler_latency.count',
        'redpanda.kafka.rpc_dispatch_handler_latency.bucket',
        'redpanda.kafka.rpc_max_service_mem_bytes.count',
        'redpanda.kafka.rpc_method_not_found_errors.count',
        'redpanda.kafka.rpc_received_bytes.count',
        'redpanda.kafka.rpc_requests_blocked_memory.count',
        'redpanda.kafka.rpc_requests_completed.count',
        'redpanda.kafka.rpc_requests_pending',
        'redpanda.kafka.rpc_sent_bytes.count',
        'redpanda.kafka.rpc_service_errors.count',
    ],
    'redpanda.leader': [
        'redpanda.leader.balancer_leader_transfer_error.count',
        'redpanda.leader.balancer_leader_transfer_no_improvement.count',
        'redpanda.leader.balancer_leader_transfer_succeeded.count',
        'redpanda.leader.balancer_leader_transfer_timeout.count',
    ],
    'redpanda.memory': [
        'redpanda.memory.allocated_memory.count',
        'redpanda.memory.cross_cpu_free_operations.count',
        'redpanda.memory.free_memory.count',
        'redpanda.memory.free_operations.count',
        'redpanda.memory.malloc_live_objects',
        'redpanda.memory.malloc_operations.count',
        'redpanda.memory.reclaims_operations.count',
        'redpanda.memory.total_memory.count',
    ],
    'redpanda.pandaproxy': [
        'redpanda.pandaproxy.request_latency.sum',
        'redpanda.pandaproxy.request_latency.count',
        'redpanda.pandaproxy.request_latency.bucket',
    ],
    'redpanda.raft': [
        'redpanda.raft.done_replicate_requests.count',
        'redpanda.raft.group_count',
        'redpanda.raft.heartbeat_requests_errors.count',
        'redpanda.raft.leader_for',
        'redpanda.raft.leadership_changes.count',
        'redpanda.raft.log_flushes.count',
        'redpanda.raft.log_truncations.count',
        'redpanda.raft.received_append_requests.count',
        'redpanda.raft.received_vote_requests.count',
        'redpanda.raft.recovery_requests_errors.count',
        'redpanda.raft.replicate_ack_all_requests.count',
        'redpanda.raft.replicate_ack_leader_requests.count',
        'redpanda.raft.replicate_ack_none_requests.count',
        'redpanda.raft.replicate_request_errors.count',
        'redpanda.raft.sent_vote_requests.count',
    ],
    'redpanda.reactor': [
        'redpanda.reactor.abandoned_failed_futures.count',
        'redpanda.reactor.aio_bytes_read.count',
        'redpanda.reactor.aio_bytes_write.count',
        'redpanda.reactor.aio_errors.count',
        'redpanda.reactor.aio_reads.count',
        'redpanda.reactor.aio_writes.count',
        'redpanda.reactor.cpp_exceptions.count',
        'redpanda.reactor.cpu_busy_ms.count',
        'redpanda.reactor.cpu_steal_time_ms.count',
        'redpanda.reactor.fstream_read_bytes.count',
        'redpanda.reactor.fstream_read_bytes_blocked.count',
        'redpanda.reactor.fstream_reads.count',
        'redpanda.reactor.fstream_reads_ahead_bytes_discarded.count',
        'redpanda.reactor.fstream_reads_aheads_discarded.count',
        'redpanda.reactor.fstream_reads_blocked.count',
        'redpanda.reactor.fsyncs.count',
        'redpanda.reactor.io_threaded_fallbacks.count',
        'redpanda.reactor.logging_failures.count',
        'redpanda.reactor.polls.count',
        'redpanda.reactor.tasks_pending',
        'redpanda.reactor.tasks_processed.count',
        'redpanda.reactor.timers_pending.count',
        'redpanda.reactor.utilization',
    ],
    'redpanda.rpc_client': [
        'redpanda.rpc_client.active_connections',
        'redpanda.rpc_client.client_correlation_errors.count',
        'redpanda.rpc_client.connection_errors.count',
        'redpanda.rpc_client.connects.count',
        'redpanda.rpc_client.corrupted_headers.count',
        'redpanda.rpc_client.in_bytes.count',
        'redpanda.rpc_client.out_bytes.count',
        'redpanda.rpc_client.read_dispatch_errors.count',
        'redpanda.rpc_client.request_errors.count',
        'redpanda.rpc_client.request_timeouts.count',
        'redpanda.rpc_client.requests.count',
        'redpanda.rpc_client.requests_blocked_memory.count',
        'redpanda.rpc_client.requests_pending',
        'redpanda.rpc_client.server_correlation_errors.count',
    ],
    'redpanda.scheduler': [
        'redpanda.scheduler.queue_length',
        'redpanda.scheduler.runtime_ms.count',
        'redpanda.scheduler.shares',
        'redpanda.scheduler.starvetime_ms.count',
        'redpanda.scheduler.tasks_processed.count',
        'redpanda.scheduler.time_spent_on_task_quota_violations_ms.count',
        'redpanda.scheduler.waittime_ms.count',
    ],
    'redpanda.stall': [
        'redpanda.stall.detector_reported.count',
    ],
    'redpanda.storage': [
        'redpanda.storage.compaction_backlog_controller_backlog_size',
        'redpanda.storage.compaction_backlog_controller_error',
        'redpanda.storage.compaction_backlog_controller_shares',
        'redpanda.storage.kvstore_cached_bytes.count',
        'redpanda.storage.kvstore_entries_fetched.count',
        'redpanda.storage.kvstore_entries_removed.count',
        'redpanda.storage.kvstore_entries_written.count',
        'redpanda.storage.kvstore_key_count.count',
        'redpanda.storage.kvstore_segments_rolled.count',
        'redpanda.storage.log_batch_parse_errors.count',
        'redpanda.storage.log_batch_write_errors.count',
        'redpanda.storage.log_batches_read.count',
        'redpanda.storage.log_batches_written.count',
        'redpanda.storage.log_cache_hits.count',
        'redpanda.storage.log_cache_misses.count',
        'redpanda.storage.log_cached_batches_read.count',
        'redpanda.storage.log_cached_read_bytes.count',
        'redpanda.storage.log_compacted_segment.count',
        'redpanda.storage.log_compaction_ratio.count',
        'redpanda.storage.log_corrupted_compaction_indices.count',
        'redpanda.storage.log_log_segments_active.count',
        'redpanda.storage.log_log_segments_created.count',
        'redpanda.storage.log_log_segments_removed.count',
        'redpanda.storage.log_partition_size',
        'redpanda.storage.log_read_bytes.count',
        'redpanda.storage.log_readers_added.count',
        'redpanda.storage.log_readers_evicted.count',
        'redpanda.storage.log_written_bytes.count',
    ],
    'redpanda.consumerlag': [
        'redpanda.consumerlag.kafka_group_offset',
    ],
}
# fmt: on

INSTANCE_DEFAULT_GROUPS = [
    'redpanda.application',
    'redpanda.cluster',
    'redpanda.httpd',
    'redpanda.kafka',
    'redpanda.leader',
    'redpanda.pandaproxy',
    'redpanda.reactor',
    'redpanda.storage',
]

INSTANCE_ADDITIONAL_GROUPS = [
    'redpanda.alien',
    'redpanda.internal_rpc',
    'redpanda.io_queue',
    'redpanda.memory',
    'redpanda.raft',
    'redpanda.rpc_client',
    'redpanda.scheduler',
    'redpanda.stall',
]


def get_metrics(metric_groups):
    """Given a list of metric groups, return single consolidated list"""
    return sorted(m for g in metric_groups for m in INSTANCE_METRIC_GROUP_MAP[g])


INSTANCE_DEFAULT_METRICS = get_metrics(INSTANCE_DEFAULT_GROUPS)
INSTANCE_ADDITIONAL_METRICS = get_metrics(INSTANCE_ADDITIONAL_GROUPS)
