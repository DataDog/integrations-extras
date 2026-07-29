# CHANGELOG - Redis Enterprise Prometheus

## 1.1.0 / 2026-07-29

***Added***:

* Expose the raw cumulative value of the `endpoint_*` Prometheus counters as gauges. These metrics
  are now submitted with the `counter_gauge` type, which adds a new `rdse2.<name>.total` gauge
  alongside the existing monotonic `rdse2.<name>.count` metric. This allows dashboards to compute
  values such as current connected clients
  (`endpoint_client_connections` - `endpoint_client_disconnections` - `endpoint_proxy_disconnections`)
  from the raw counter totals. The existing `.count` metrics are unchanged.
* Add `rdse2.redis_server_db_keys`, a distinct wire gauge for the total key count.

***Deprecated***:

* `rdse2.redis_server_db0_keys` is deprecated in favor of `rdse2.redis_server_db_keys`. It remains
  mapped and emitting for backward compatibility, and dashboards now reference
  `rdse2.redis_server_db_keys`.

## 1.0.1 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [#2829](https://github.com/DataDog/integrations-extras/pull/2829)

## 1.0.0 / 2025-09-22

***Added***:

* Initial Release

