# CHANGELOG - PureFA

## 1.2.0/ 2023-11-13

***Added***:

* Added support for the `purefa.pod.replica_links_lag_average_sec` metric introduced in `pure-fb-openmetrics-exporter v1.0.4`.
* Added support for the `purefa.pod.replica_links_lag_max_sec` metric introduced in `pure-fb-openmetrics-exporter v1.0.4`.
* Added support for the `purefa.pod.replica_links_performance_bandwidth_bytes` metric introduced in `pure-fb-openmetrics-exporter v1.0.4`.
* Added support for the `purefa.pod.performance_replication_bandwidth_bytes` metric introduced in `pure-fb-openmetrics-exporter v1.0.4`.
* Added support for the `purefa.network.interface_performance_bandwidth_bytes` metric introduced in `pure-fb-openmetrics-exporter v1.0.5`.
* Added support for the `purefa.network.interface_performance_throughput_pkts` metric introduced in `pure-fb-openmetrics-exporter v1.0.5`.
* Added support for the `purefa.network.interface_performance_errors` metric introduced in `pure-fb-openmetrics-exporter v1.0.5`.
* Added support for the `purefa.host.connectivity_info` metric introduced in `pure-fb-openmetrics-exporter v1.0.10`.
* Added support for the `purefa.drive.capacity_bytes` metric introduced in `pure-fb-openmetrics-exporter v1.0.11`.

***Fixed***:

* Bump the minimum base check version to 33.1.0 ([2184](https://github.com/DataDog/integrations-extras/pull/2184))

## 1.1.1 / 2023-04-28

***Fixed***:

* Remove the use_latest_spec option from the config file ([#1835](https://github.com/DataDog/integrations-extras/pull/1835))

## 1.1.0

***Deprecated***:

* Support for the [Pure Exporter](https://github.com/PureStorage-OpenConnect/pure-exporter) - Deprecated metrics names are listed in `metadata.csv` as `Legacy`

***Added***:

* Support for [Pure FlashArray OpenMetrics Exporter](https://github.com/PureStorage-OpenConnect/pure-fa-openmetrics-exporter)

## 1.0.1

***Fixed***:

* Updated purefa.py to include a default `openmetrics_endpoint` from `spec.yaml`

## 1.0.0

***Added***:

* Initial Pure Storage FlashArray integration.
