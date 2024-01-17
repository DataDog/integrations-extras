# CHANGELOG - hikaricp

## 1.2.0 / 2024-01-16

***Added***:
* Added collection for prometheus-style named metrics:
  * hikaricp_active_connections
  * hikaricp_idle_connections
  * hikaricp_max_connections
  * hikaricp_min_connections
  * hikaricp_pending_threads
  * hikaricp_connection_timeout
  * hikaricp_connection_acquired_nanos
  * hikaricp_connection_creation_millis
  * hikaricp_connection_usage_millis

## 1.1.1 / 2023-10-31

***Changed***:

* Config models update - PR [2088](https://github.com/DataDog/integrations-extras/pull/2088)

## 1.1.0 / 2023-08-09

***Added***:

* Added hikaricp.connections.max (pool max size) ([#1890](https://github.com/DataDog/integrations-extras/pull/1890). Thanks [styner9](https://github.com/styner9))

***Fixed***:

* Add DEFAULT_METRIC_LIMIT = 0 for OpenMetrics-based integrations ([#1843](https://github.com/DataDog/integrations-extras/pull/1843))

## 1.0.1 / 2023-04-28

***Fixed***:

* Remove the use_latest_spec option from the config file ([#1835](https://github.com/DataDog/integrations-extras/pull/1835))

## 1.0.0

***Added***:

* Initial Hikaricp Integration.
