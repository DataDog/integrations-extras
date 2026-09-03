# CHANGELOG - Redis Enterprise Prometheus

## 1.2.0 / 2026-08-26

***Added***:

* Collect `rdse2.node_uname_info` and `rdse2.node_config`. Both were already documented in `metadata.csv` but were missing from the check's metric map, so they were never emitted. `node_uname_info` carries the per-node `nodename` label (the internal hostname) and `node_config` carries `rs_version`. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)

***Fixed***:

* Point the Database List widgets at `rdse2.db_config` instead of `rdse2.database_syncer_config`. The latter is a configuration-label placeholder that only exists on Active-Active deployments and lives in the opt-in `REDIS2.REPLICATION` group, so the widget was empty on a default install. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Add the missing `.count` suffix to the `rdse2.endpoint_ingress` / `rdse2.endpoint_egress` queries in the Database Input/Output widget. These are Prometheus counters, which the OpenMetrics v2 check emits as `.count`. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Compute current connections from the `.total` gauges and subtract `rdse2.endpoint_proxy_disconnections.total`, rather than differencing two monotonic `.count` deltas. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Stop dividing by time twice in the Database Input/Output, Shard Process CPU, and Proxy Threads CLI Session widgets, which wrapped an already-rated (`.as_rate()`) query in `per_second()` / `derivative()`. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Un-swap the ingress and egress series labels (and the accompanying note text) in the Database Input/Output widget. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Rebuild the Node Latency widget as a calculated field over the `endpoint_*_requests_latency_histogram` sum/count pairs. It previously queried `rdse.node_avg_latency`, a V1-only metric under the wrong namespace. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Group the Cluster Nodes widget by `nodename` from `rdse2.node_uname_info` instead of the non-existent `internal-hostname` tag. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Remove the Node Network Traffic widget; both `rdse.node_egress_bytes_median` and `rdse.node_ingress_bytes_median` are V1-only metrics with no V2 equivalent. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)
* Remove `title` from `note` widgets, folding it into the note content as a markdown heading. The Dashboards API rejects `title` on notes, which made the dashboard assets fail to import. [#3136](https://github.com/DataDog/integrations-extras/pull/3136)

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

