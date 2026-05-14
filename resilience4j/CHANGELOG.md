# CHANGELOG - Resilience4j

## 1.1.1 / 2025-09-25

***Fixed***:

* Updated minimum `datadog-checks-base` version from 32.6.0 to 37.0.0 to fix Python 3.12 compatibility issues in CI pipeline
* Fixed e2e tests to properly handle OpenMetrics check behavior for connection errors

## 1.1.0 / 2025-08-20

***Added***:

* Added missing CircuitBreaker metrics: `not.permitted.calls` and `slow.call.rate`
* Added missing Bulkhead metric: `core.thread.pool.size`

## 1.0.0 / 2025-01-24

***Added***:

* Initial Release
