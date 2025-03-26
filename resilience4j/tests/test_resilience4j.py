import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.resilience4j import Resilience4jCheck

EXPECTED_PROMETHEUS_METRICS = {
    "bulkhead.available.concurrent.calls",
    "bulkhead.max.allowed.concurrent.calls",
    "bulkhead.max.thread.pool.size",
    "bulkhead.queue.capacity",
    "bulkhead.queue.depth",
    "bulkhead.thread.pool.size",
    "circuitbreaker.buffered.calls",
    "circuitbreaker.calls.seconds.count",
    "circuitbreaker.calls.seconds.max",
    "circuitbreaker.calls.seconds.sum",
    "circuitbreaker.calls",
    "circuitbreaker.failure.rate",
    "circuitbreaker.max.buffered.calls",
    "circuitbreaker.state",
    "ratelimiter.available.permissions",
    "ratelimiter.waiting.threads",
    "retry.calls",
    "timelimiter.calls",
}


@pytest.mark.integration
def test_check(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=0)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("resilience4j.prometheus.health", status=Resilience4jCheck.OK)
