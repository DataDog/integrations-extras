# CHANGELOG - celerdata

## 1.3.0 / 2026-09-30

***Added***:

* Add the `celerdata.fe.slow_lock_held_time_ms` and `celerdata.fe.slow_lock_wait_time_ms` metrics, which report FE slow-lock held and wait times as quantiles plus a sample count (requires StarRocks 3.5.10 or later, or 4.0.3 or later)

***Fixed***:

* Collect all per-database `celerdata.fe.table_num` series. Previously, only the first database was reported. Queries and monitors that don't group this metric by `db_name` now aggregate across every database.

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