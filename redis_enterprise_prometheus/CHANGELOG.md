# CHANGELOG - Redis Enterprise Prometheus

## 1.2.0 / 2026-08-31

***Added***:

* Add the "Redis Enterprise Prometheus - Redis Cloud Database" dashboard, which visualizes database-level metrics for Redis Cloud deployments. It is scoped by the Redis Cloud `sub_id` and `db_name` tags rather than the `cluster` and `db` tags used by the Redis Enterprise Software dashboards.

## 1.1.0 / 2026-07-29

***Deprecated***:

* Deprecate `rdse2.redis_server_db0_keys` in favor of `rdse2.redis_server_db_keys`; it remains mapped and emitting for backward compatibility. [#3078](https://github.com/DataDog/integrations-extras/pull/3078)

***Added***:

* Submit the client-connection `endpoint_*` counters with the `counter_gauge` type, adding `.total` gauges (`rdse2.endpoint_client_connections.total`, `rdse2.endpoint_client_disconnections.total`, `rdse2.endpoint_proxy_disconnections.total`) alongside the existing `.count` metrics so current connected clients can be computed from the raw totals. [#3078](https://github.com/DataDog/integrations-extras/pull/3078)
* Add `rdse2.redis_server_db_keys`, a distinct gauge for the total key count. [#3078](https://github.com/DataDog/integrations-extras/pull/3078)

***Fixed***:

* Rename the internal `get_default_config` method so it no longer collides with the method `OpenMetricsBaseCheckV2` added in datadog-checks-base 37.39.0, which crashed the check on recent Agents. [#3078](https://github.com/DataDog/integrations-extras/pull/3078)

## 1.0.1 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [#2829](https://github.com/DataDog/integrations-extras/pull/2829)

## 1.0.0 / 2025-09-22

***Added***:

* Initial Release

