# CHANGELOG - celerdata

## 1.2.2 / 2026-06-03

***Fixed***:

* Collect all per-database `starrocks_fe_table_num` series. StarRocks FE exposes this metric interleaved with `starrocks_fe_db_size_bytes`, so the OpenMetrics parser typed every series after the first as `unknown` and dropped them; pinning the metric type to `gauge` recovers all per-db series.

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