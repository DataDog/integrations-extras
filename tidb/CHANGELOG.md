# CHANGELOG - TiDB

## 2.2.0 / 2026-04-19

***Added***:

* Add `tiflash_syncing_data_freshness` histogram metric to track TiFlash replication lag from TiKV ([#XXXX](https://github.com/DataDog/integrations-extras/pull/XXXX))
* Add PD client metrics: `pd_client_cmd_handle_cmds_duration_seconds` and `pd_client_request_handle_requests_duration_seconds`
* Add TiDB session phase duration metrics: `tidb_session_parse_duration_seconds`, `tidb_session_compile_duration_seconds`, `tidb_session_execute_duration_seconds`, `tidb_session_transaction_duration_seconds`
* Add TiDB connection metrics: `tidb_server_get_token_duration_seconds`, `tidb_server_conn_idle_duration_seconds`
* Add TiDB server metrics: `tidb_server_query_total`, `tidb_server_disconnection_total`, `tidb_server_plan_cache_total`, `tidb_server_plan_cache_miss_total`
* Add TiDB TiKV client metric: `tidb_tikvclient_request_seconds`
* Add TiKV raftstore metrics: `tikv_raftstore_append_log_duration_seconds`, `tikv_raftstore_apply_log_duration_seconds`, `tikv_raftstore_commit_log_duration_seconds`, `tikv_raftstore_store_duration_secs`, `tikv_raftstore_apply_duration_secs`
* Add TiKV storage and gRPC metrics: `tikv_storage_engine_async_request_duration_seconds`, `tikv_grpc_msg_duration_seconds`, `tikv_engine_flow_bytes`, `tikv_thread_cpu_seconds_total`
* Add unit tests and fixture data for all new metrics

## 2.1.1 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [#2829](https://github.com/DataDog/integrations-extras/pull/2829)

## 2.1.0 / 2021-11-30

***Added***:

* Update default metrics.
* Update the default dashboard.
* Expose the `metrics` mapper config to let users customize more metrics.
* Let users to customize metric namespace.
* Add more tests.

## 2.0.0 / 2021-10-13

***Removed***:

* Removed the useless service monitor.
* Removed buggy `auto_conf.yaml`.

***Changed***:

* Made the one screen dashboard better.
* Improved the readme document.
* Added integration tests.
* Refactored unit tests.
* Refactored integration configurations.

***Added***:

* Added a service check.

## 1.0.0 / 2021-05-25

***Removed***:

* Removed useless monitor.

***Added***:

* Made user doc more understandable.

## 0.1.0 / 2021-05-10

***Added***:

* Added TiDB integration.
