# CHANGELOG - PureFB

## 2.0.1 / 2024-07-22

* Renamed incorrectly named metric to correctly align with metrics namings and instrument standards.
`purefb.clients_performance_average_bytes` to `purefb.clients.performance_average_bytes`

## 2.0.0 / 2024-06-26

***Added***: 

* Added support for metrics that were implemented in the FlashBlade OpenMetrics Exporter:
`purefb.array.performance_replication`
`purefb.buckets.quota_space_bytes`
`purefb.buckets.object_count`

***Fixed***:

* Renamed metrics to align with the standards of the FlashBlade OpenMetrics Exporter v1.0.11+ so that they would be correctly consumed
`purefb.array.clients_performance_avg_size_bytes` to `purefb.clients_performance_average_bytes`
`purefb.array.clients_performance_bandwidth_bytes` to `purefb.clients.performance_bandwidth_bytes`
`purefb.array.clients_performance_latency_usec` to `purefb.clients.performance_latency_usec`
`purefb.array.clients_performance_throughput_iops` to `purefb.clients.performance_throughput_iops`
`purefb.array.nfs_latency_usec` to `purefb.array.nfs_specific_performance_latency_usec`
`purefb.array.nfs_throughput_iops` to `purefb.array.nfs_specific_performance_throughput_iops`

* Removed deprecated metrics that have been removed from the FlashBlade OpenMetrics Exporter v1.0.0+
`purefb.bucket.replica_links_lag_msec` 
`purefb.buckets.space_objects`
`purefb.file.system_links_lag_msec`

## 1.0.4 / 2023-10-31

***Added***:

* Added support for the `purefb.nfs.export_rule` metric introduced in `pure-fb-openmetrics-exporter v1.0.3`.

## 1.0.3 / 2023-04-28

***Fixed***:

* Remove the use_latest_spec option from the config file ([#1835](https://github.com/DataDog/integrations-extras/pull/1835))

## 1.0.2 / 2022-12-14

***Added***:

* Added support for the `purefb.array.space_utilization` metric introduced in `pure-fb-openmetrics-exporter v1.0.1`.

## 1.0.1 / 2022-10-04

***Fixed***:

* Fixed the link for Pure Storage Logo on the `Pure FlashBlade - Overview` dashboard.

## 1.0.0 / 2022-05-04

***Added***:

* Initial Pure Storage FlashBlade integration.
