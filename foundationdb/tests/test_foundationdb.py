
from typing import Any, Dict

from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.base import AgentCheck
from datadog_checks.foundationdb import FoundationdbCheck

METRICS = [
    "foundationdb.latency_probe.batch_priority_transaction_start_seconds",
    "foundationdb.latency_probe.commit_seconds",
    "foundationdb.latency_probe.immediate_priority_transaction_start_seconds",
    "foundationdb.latency_probe.read_seconds",
    "foundationdb.latency_probe.transaction_start_seconds",
    "foundationdb.machines",
    "foundationdb.processes",
    "foundationdb.degraded_processes",
    "foundationdb.workload.transactions.committed.counter",
    "foundationdb.workload.transactions.committed.hz",
    "foundationdb.workload.transactions.conflicted.counter",
    "foundationdb.workload.transactions.conflicted.hz",
    "foundationdb.workload.transactions.rejected_for_queued_too_long.counter",
    "foundationdb.workload.transactions.rejected_for_queued_too_long.hz",
    "foundationdb.workload.transactions.started.counter",
    "foundationdb.workload.transactions.started.hz",
    "foundationdb.workload.transactions.started_batch_priority.counter",
    "foundationdb.workload.transactions.started_batch_priority.hz",
    "foundationdb.workload.transactions.started_default_priority.counter",
    "foundationdb.workload.transactions.started_default_priority.hz",
    "foundationdb.workload.transactions.started_immediate_priority.counter",
    "foundationdb.workload.transactions.started_immediate_priority.hz",
    "foundationdb.workload.operations.location_requests.counter",
    "foundationdb.workload.operations.location_requests.hz",
    "foundationdb.workload.operations.low_priority_reads.counter",
    "foundationdb.workload.operations.low_priority_reads.hz",
    "foundationdb.workload.operations.memory_errors.counter",
    "foundationdb.workload.operations.memory_errors.hz",
    "foundationdb.workload.operations.read_requests.counter",
    "foundationdb.workload.operations.read_requests.hz",
    "foundationdb.workload.operations.reads.counter",
    "foundationdb.workload.operations.reads.hz",
    "foundationdb.workload.operations.writes.counter",
    "foundationdb.workload.operations.writes.hz",
    "foundationdb.data.system_kv_size_bytes",
    "foundationdb.data.total_disk_used_bytes",
    "foundationdb.data.total_kv_size_bytes",
    "foundationdb.data.least_operating_space_bytes_log_server",
    "foundationdb.data.moving_data.in_flight_bytes",
    "foundationdb.data.moving_data.in_queue_bytes",
    "foundationdb.data.moving_data.total_written_bytes",
    "foundationdb.datacenter_lag.seconds",
    "foundationdb.instances",
]

def test_check(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = FoundationdbCheck('foundationdb', {}, [instance])
    check.check(instance)

    for metric in METRICS:
        aggregator.assert_metric(metric)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("foundationdb.can_connect", AgentCheck.OK)
