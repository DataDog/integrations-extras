import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.resilience4j import Resilience4jCheck

# EXPECTED_MICROMETER_METRICS = {
#     "resilience4j.bulkhead.available.concurrent.calls",
#     "resilience4j.bulkhead.max.allowed.concurrent.calls",
#     "resilience4j.bulkhead.max.thread.pool.size",
#     "resilience4j.bulkhead.queue.capacity",
#     "resilience4j.bulkhead.queue.depth",
#     "resilience4j.bulkhead.thread.pool.size",
#     "resilience4j.circuitbreaker.buffered.calls",
#     "resilience4j.circuitbreaker.calls.seconds.count",
#     "resilience4j.circuitbreaker.calls.seconds.max",
#     "resilience4j.circuitbreaker.calls.seconds.sum",
#     # "resilience4j.circuitbreaker.calls",
#     "resilience4j.circuitbreaker.failure.rate",
#     "resilience4j.circuitbreaker.max.buffered.calls",
#     "resilience4j.circuitbreaker.state",
#     "resilience4j.ratelimiter.available.permissions",
#     "resilience4j.ratelimiter.waiting.threads",
#     "resilience4j.retry.calls",
#     "resilience4j.timelimiter.calls.count",
# }

EXPECTED_PROMETHEUS_METRICS = {
    "resilience4j.bulkhead.available.concurrent.calls",
    "resilience4j.bulkhead.max.allowed.concurrent.calls",
    "resilience4j.bulkhead.max.thread.pool.size",
    "resilience4j.bulkhead.queue.capacity",
    "resilience4j.bulkhead.queue.depth",
    "resilience4j.bulkhead.thread.pool.size",
    "resilience4j.circuitbreaker.buffered.calls",
    "resilience4j.circuitbreaker.calls.seconds.count",
    "resilience4j.circuitbreaker.calls.seconds.max",
    "resilience4j.circuitbreaker.calls.seconds.sum",
    "resilience4j.circuitbreaker.calls",
    "resilience4j.circuitbreaker.failure.rate",
    "resilience4j.circuitbreaker.max.buffered.calls",
    "resilience4j.circuitbreaker.state",
    "resilience4j.ratelimiter.available.permissions",
    "resilience4j.ratelimiter.waiting.threads",
    "resilience4j.retry.calls",
    "resilience4j.timelimiter.calls",
}


# @pytest.mark.unit
# def test_mock_assert_micrometer_metrics(dd_run_check, aggregator, check, mock_micrometer_metrics):
#     dd_run_check(check)
#     for metric_name in EXPECTED_MICROMETER_METRICS:
#         aggregator.assert_metric(metric_name)
#     aggregator.assert_all_metrics_covered()
#     aggregator.assert_metrics_using_metadata(get_metadata_metrics())
#     aggregator.assert_service_check("resilience4j.openmetrics.health", status=Resilience4jCheck.OK)


@pytest.mark.unit
def test_mock_assert_prometheus_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    # aggregator.assert_service_check("resilience4j.openmetrics.health", status=Resilience4jCheck.OK)