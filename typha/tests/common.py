# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.stubs import aggregator

EXPECTED_METRICS = {
    'typha.cache.size': aggregator.GAUGE,
    'typha.snapshots.generated': aggregator.MONOTONIC_COUNT,
    'typha.snapshots.reused': aggregator.MONOTONIC_COUNT,
    'typha.snapshot.raw.bytes': aggregator.GAUGE,
    'typha.snapshots.compressed.bytes': aggregator.GAUGE,
    'typha.breadcrumb.block': aggregator.MONOTONIC_COUNT,
    'typha.breadcrumb.non.block': aggregator.MONOTONIC_COUNT,
    'typha.breadcrumb.seq.number': aggregator.GAUGE,
    'typha.breadcrumb.size.count': aggregator.MONOTONIC_COUNT,
    'typha.breadcrumb.size.sum': aggregator.MONOTONIC_COUNT,
    'typha.client.latency.secs.count': aggregator.MONOTONIC_COUNT,
    'typha.client.latency.secs.sum': aggregator.MONOTONIC_COUNT,
    'typha.client.snapshot.send.secs.count': aggregator.MONOTONIC_COUNT,
    'typha.client.snapshot.send.secs.sum': aggregator.MONOTONIC_COUNT,
    'typha.client.write.latency.secs.count': aggregator.MONOTONIC_COUNT,
    'typha.client.write.latency.secs.sum': aggregator.MONOTONIC_COUNT,
    'typha.connections.accepted': aggregator.MONOTONIC_COUNT,
    'typha.connections.active': aggregator.GAUGE,
    'typha.connections.streaming': aggregator.GAUGE,
    'typha.connections.dropped': aggregator.MONOTONIC_COUNT,
    'typha.kvs.per.msg.count': aggregator.MONOTONIC_COUNT,
    'typha.kvs.per.msg.sum': aggregator.MONOTONIC_COUNT,
    'typha.log.errors': aggregator.MONOTONIC_COUNT,
    'typha.logs.dropped': aggregator.MONOTONIC_COUNT,
    'typha.next.breadcrumb.latency.secs.count': aggregator.MONOTONIC_COUNT,
    'typha.next.breadcrumb.latency.secs.sum': aggregator.MONOTONIC_COUNT,
    'typha.ping.latency.count': aggregator.MONOTONIC_COUNT,
    'typha.ping.latency.sum': aggregator.MONOTONIC_COUNT,
    'typha.updates.skipped': aggregator.MONOTONIC_COUNT,
    'typha.updates.total': aggregator.MONOTONIC_COUNT,
}


EXPECTED_CHECKS = {
    'typha.prometheus.health',
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/metrics',
}
