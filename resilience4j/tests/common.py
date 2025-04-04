# Constants

INSTANCE = {"openmetrics_endpoint": "http://127.0.0.1:9080/actuator/prometheus"}

BAD_HOSTNAME_INSTANCE = {"openmetrics_endpoint": "http://invalid-hostname"}

EXPECTED_PROMETHEUS_METRICS = {
    "resilience4j.bulkhead.available.concurrent.calls",
    "resilience4j.bulkhead.max.allowed.concurrent.calls",
    "resilience4j.bulkhead.max.thread.pool.size",
    "resilience4j.bulkhead.queue.capacity",
    "resilience4j.bulkhead.queue.depth",
    "resilience4j.bulkhead.thread.pool.size",
    "resilience4j.circuitbreaker.buffered.calls",
    "resilience4j.circuitbreaker.calls.seconds.bucket",
    "resilience4j.circuitbreaker.calls.seconds.count",
    "resilience4j.circuitbreaker.calls.seconds.max",
    "resilience4j.circuitbreaker.calls.seconds.sum",
    "resilience4j.circuitbreaker.calls",
    "resilience4j.circuitbreaker.failure.rate",
    "resilience4j.circuitbreaker.max.buffered.calls",
    "resilience4j.circuitbreaker.state",
    "resilience4j.ratelimiter.available.permissions",
    "resilience4j.ratelimiter.waiting.threads",
    "resilience4j.retry.calls.count",
    "resilience4j.retry.calls",
    "resilience4j.timelimiter.calls",
}
