METRICS_MAP = {
        'grpc_server_handled_total': 'grpc.server.handled.total',
        'grpc_server_handling_seconds_bucket': 'grpc.server.handling.seconds.bucket',
        'grpc_server_handling_seconds_count': 'grpc.server.handling.seconds.count',
        'grpc_server_handling_seconds_sum': 'grpc.server.handling.seconds.sum',
        'grpc_server_msg_received_total': 'grpc.server.msg.received.total',
        'grpc_server_msg_sent_total': 'grpc.server.msg.sent.total',
        'grpc_server_started_total': 'grpc.server.started.total',
        'process_cpu_seconds_total': 'process.cpu.seconds.total',
        'process_virtual_memory_bytes': 'process.virtual.memory.bytes',
        'spicedb_audit_batch_send_latency_bucket': 'spicedb.audit.batch.send.latency.bucket',
        'spicedb_audit_batch_send_latency_count': 'spicedb.audit.batch.send.latency.count',
        'spicedb_audit_batch_send_latency_sum': 'spicedb.audit.batch.send.latency.sum',
        'spicedb_audit_batch_size_bucket': 'spicedb.audit.batch.size.bucket',
        'spicedb_audit_batch_size_count': 'spicedb.audit.batch.size.count',
        'spicedb_audit_batch_size_sum': 'spicedb.audit.batch.size.sum',
        'spicedb_audit_buffer_size_bucket': 'spicedb.audit.buffer.size.bucket',
        'spicedb_audit_buffer_size_count': 'spicedb.audit.buffer.size.count',
        'spicedb_audit_buffer_size_sum': 'spicedb.audit.buffer.size.sum',
        'spicedb_audit_buffer_spilled': 'spicedb.audit.buffer.spilled',
        'spicedb_audit_delivery_attempt': 'spicedb.audit.delivery.attempt',
        'spicedb_audit_delivery_failure': 'spicedb.audit.delivery.failure',
        'spicedb_audit_failures_per_batch_bucket': 'spicedb.audit.failures.per.batch.bucket',
        'spicedb_audit_failures_per_batch_count': 'spicedb.audit.failures.per.batch.count',
        'spicedb_audit_failures_per_batch_sum': 'spicedb.audit.failures.per.batch.sum',
        'spicedb_audit_send_latency_bucket': 'spicedb.audit.send.latency.bucket',
        'spicedb_audit_send_latency_count': 'spicedb.audit.send.latency.count',
        'spicedb_audit_send_latency_sum': 'spicedb.audit.send.latency.sum',
        'spicedb_audit_worker_unavailable': 'spicedb.audit.worker.unavailable',
        }

def construct_metric_config(raw: str, dotted: str):
    """
    Transforms openmetrics configuration names into names that datadog likes.
    """
    if raw.endswith('_total'):
        raw = raw[:-6]
        dotted = dotted[:-6]
    elif dotted.endswith('.count'):
        dotted = dotted[:-6]

    return {raw: {'name': dotted}}

METRICS_CONFIG = [
        construct_metric_config(raw, dotted) for raw, dotted in METRICS_MAP.items()
        ]
