# CHANGELOG - celerdata

## 1.3.0 / 2026-09-25

***Added***:

* Add the `celerdata.fe.slow_lock_held_time_ms` and `celerdata.fe.slow_lock_wait_time_ms` summary metrics, surfacing FE slow-lock held and wait times (introduced by StarRocks/starrocks#66027)

***Fixed***:

* Collect all per-database `celerdata.fe.table_num` series. StarRocks FE interleaves this metric with `starrocks_fe_db_size_bytes`, so the OpenMetrics parser typed every series after the first as `unknown` and dropped them; pinning the metric type to `gauge` recovers every per-database series.

## 1.2.1 / 2025-10-01

***Fixed***:

* Since StarRocks FE has fixed the metrics format issue, now it is needed to restore the deleted test case.

## 1.2.0 / 2025-06-30

***Added***:

* Add the `celerdata.fe.routine_load_max_lag_of_partition` metric

## 1.1.0 / 2025-02-21

***Added***:

* Add a grok expression to parse the new log format of BE

## 1.0.0 / 2024-03-11

***Added***:

* Initial Release
* StarRocks provides a Prometheus-compatible information collection interface, and this integration collects metrics and logs from StarRocks.