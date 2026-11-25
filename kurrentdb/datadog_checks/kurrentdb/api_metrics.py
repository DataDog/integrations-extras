# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# Metrics read from KurrentDB's JSON HTTP API. These carry over the metrics of the deprecated `eventstore`
# integration and cover data that is not exposed on the Prometheus `/metrics` endpoint, such as cluster
# membership.
#
# Each endpoint maps to a list of groups: (path to the objects, tags taken from each object, metrics).
# The path is '' for the response itself. A list at the path yields one object per element, and a dict
# yields one object per value when `many` is set. Each metric is (json field, metric name, kind).

NUMBER = 'number'
BOOL = 'bool'
DURATION = 'duration'


def equals(value):
    return ('equals', value)


API_ENDPOINTS = {
    '/stats': [
        {
            'path': '',
            'metrics': [
                ('proc.mem', 'proc.mem', NUMBER),
                ('proc.cpu', 'proc.cpu', NUMBER),
                ('proc.threadsCount', 'proc.threads', NUMBER),
                ('proc.contentionsRate', 'proc.contentions_rate', NUMBER),
                ('proc.thrownExceptionsRate', 'proc.thrown_exceptions_rate', NUMBER),
                ('proc.diskIo.readBytes', 'proc.disk.read_bytes', NUMBER),
                ('proc.diskIo.writtenBytes', 'proc.disk.write_bytes', NUMBER),
                ('proc.diskIo.readOps', 'proc.disk.read_ops', NUMBER),
                ('proc.diskIo.writeOps', 'proc.disk.write_ops', NUMBER),
                ('proc.tcp.connections', 'tcp.connections', NUMBER),
                ('proc.tcp.receivingSpeed', 'tcp.receiving_speed', NUMBER),
                ('proc.tcp.sendingSpeed', 'tcp.sending_speed', NUMBER),
                ('proc.tcp.inSend', 'tcp.in_send', NUMBER),
                ('proc.tcp.measureTime', 'tcp.measure_time', DURATION),
                ('proc.tcp.pendingReceived', 'tcp.pending_received', NUMBER),
                ('proc.tcp.pendingSend', 'tcp.pending_send', NUMBER),
                ('proc.tcp.receivedBytesSinceLastRun', 'tcp.received_bytes.since_last_run', NUMBER),
                ('proc.tcp.receivedBytesTotal', 'tcp.received_bytes.total', NUMBER),
                ('proc.tcp.sentBytesSinceLastRun', 'tcp.sent_bytes.since_last_run', NUMBER),
                ('proc.tcp.sentBytesTotal', 'tcp.sent_bytes.total', NUMBER),
                ('proc.gc.allocationSpeed', 'gc.allocation_speed', NUMBER),
                ('proc.gc.gen0ItemsCount', 'gc.items_count.gen0', NUMBER),
                ('proc.gc.gen0Size', 'gc.size.gen0', NUMBER),
                ('proc.gc.gen1ItemsCount', 'gc.items_count.gen1', NUMBER),
                ('proc.gc.gen1Size', 'gc.size.gen1', NUMBER),
                ('proc.gc.gen2ItemsCount', 'gc.items_count.gen2', NUMBER),
                ('proc.gc.gen2Size', 'gc.size.gen2', NUMBER),
                ('proc.gc.largeHeapSize', 'gc.large_heap_size', NUMBER),
                ('proc.gc.timeInGc', 'gc.time_in_gc', NUMBER),
                ('proc.gc.totalBytesInHeaps', 'gc.total_bytes_in_heaps', NUMBER),
                ('sys.freeMem', 'sys.free_mem', NUMBER),
                ('es.writer.lastFlushSize', 'es.writer.flush_size.last', NUMBER),
                ('es.writer.lastFlushDelayMs', 'es.writer.flush_delay_ms.last', NUMBER),
                ('es.writer.meanFlushSize', 'es.writer.flush_size.mean', NUMBER),
                ('es.writer.meanFlushDelayMs', 'es.writer.flush_delay_ms.mean', NUMBER),
                ('es.writer.maxFlushSize', 'es.writer.flush_size.max', NUMBER),
                ('es.writer.maxFlushDelayMs', 'es.writer.flush_delay_ms.max', NUMBER),
                ('es.writer.queuedFlushMessages', 'es.writer.queued_flush_messages', NUMBER),
                ('es.readIndex.cachedRecord', 'es.read_index.cached_record', NUMBER),
                ('es.readIndex.notCachedRecord', 'es.read_index.not_cached_record', NUMBER),
                ('es.readIndex.cachedStreamInfo', 'es.read_index.cached_stream_info', NUMBER),
                ('es.readIndex.notCachedStreamInfo', 'es.read_index.not_cached_stream_info', NUMBER),
                ('es.readIndex.cachedTransInfo', 'es.read_index.cached_trans_info', NUMBER),
                ('es.readIndex.notCachedTransInfo', 'es.read_index.not_cached_trans_info', NUMBER),
            ],
        },
        {
            'path': 'es.queue',
            'many': True,
            'tags': {'queue_name': 'queueName', 'group_name': 'groupName'},
            'metrics': [
                ('avgItemsPerSecond', 'es.queue.avg_items_per_second', NUMBER),
                ('avgProcessingTime', 'es.queue.avg_processing_time', NUMBER),
                ('currentIdleTime', 'es.queue.current_idle_time', DURATION),
                ('currentItemProcessingTime', 'es.queue.current_processing_time', DURATION),
                ('idleTimePercent', 'es.queue.idle_time_percent', NUMBER),
                ('length', 'es.queue.length', NUMBER),
                ('lengthCurrentTryPeak', 'es.queue.length_current_try_peak', NUMBER),
                ('lengthLifetimePeak', 'es.queue.length_lifetime_peak', NUMBER),
                ('totalItemsProcessed', 'es.queue.total_items_processed', NUMBER),
            ],
        },
    ],
    '/info': [
        {
            'path': '',
            'metrics': [
                ('state', 'is_leader', equals('leader')),
                ('state', 'is_follower', equals('follower')),
                ('state', 'is_readonlyreplica', equals('readonlyreplica')),
            ],
        },
    ],
    '/projections/all-non-transient': [
        {
            'path': 'projections',
            'tags': {'projection': 'effectiveName'},
            'metrics': [
                ('coreProcessingTime', 'projection.core_processing_time', NUMBER),
                ('version', 'projection.version', NUMBER),
                ('epoch', 'projection.epoch', NUMBER),
                ('readsInProgress', 'projection.reads_in_progress', NUMBER),
                ('writesInProgress', 'projection.writes_in_progress', NUMBER),
                ('partitionsCached', 'projection.partitions_cached', NUMBER),
                ('status', 'projection.running', equals('Running')),
                ('progress', 'projection.progress', NUMBER),
                ('eventsProcessedAfterRestart', 'projection.events_processed_after_restart', NUMBER),
                ('bufferedEvents', 'projection.buffered_events', NUMBER),
                ('writePendingEventsBeforeCheckpoint', 'projection.write_pending_events_before_checkpoint', NUMBER),
                ('writePendingEventsAfterCheckpoint', 'projection.write_pending_events_after_checkpoint', NUMBER),
            ],
        },
    ],
    '/subscriptions': [
        {
            'path': '',
            'tags': {'event_stream_id': 'eventStreamId', 'group_name': 'groupName'},
            'metrics': [
                ('status', 'subscription.live', equals('Live')),
                ('averageItemsPerSecond', 'subscription.average_items_per_second', NUMBER),
                ('totalItemsProcessed', 'subscription.items_processed', NUMBER),
                ('lastProcessedEventNumber', 'subscription.last_processed_event_number', NUMBER),
                ('lastKnownEventNumber', 'subscription.last_known_event_number', NUMBER),
                ('connectionCount', 'subscription.connections', NUMBER),
                ('totalInFlightMessages', 'subscription.messages_in_flight', NUMBER),
            ],
        },
    ],
    '/gossip': [
        {
            'path': 'members',
            'tags': {'http_end_point_ip': 'httpEndPointIp', 'http_end_point_port': 'httpEndPointPort'},
            'metrics': [
                ('isAlive', 'cluster.member_alive', BOOL),
                ('lastCommitPosition', 'cluster.last_commit_position', NUMBER),
                ('writerCheckpoint', 'cluster.writer_checkpoint', NUMBER),
                ('chaserCheckpoint', 'cluster.chaser_checkpoint', NUMBER),
                ('epochPosition', 'cluster.epoch_position', NUMBER),
                ('epochNumber', 'cluster.epoch_number', NUMBER),
                ('nodePriority', 'cluster.node_priority', NUMBER),
            ],
        },
    ],
}

DEFAULT_ENDPOINTS = ['/stats', '/info', '/projections/all-non-transient', '/subscriptions', '/gossip']
