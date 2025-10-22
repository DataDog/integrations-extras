# CHANGELOG - redpanda

## 2.2.0 / 2025-10-21

Metrics update release.

***Changed***:

* Set `histogram_buckets_as_distributions` to true by default to send histogram buckets as Datadog distribution metrics

***Added***:

* Added new default metrics groups:
  * Security and TLS
    * `redpanda.authorization`: +1 metric
    * `redpanda.security`: +2 metrics
    * `redpanda.tls`: +5 metrics

* Added new additional metrics groups:
  * Apache Iceberg integration
    * `redpanda.iceberg`: +32 metrics
  * Redpanda Transforms and WASM
    * `redpanda.transform`: +9 metrics
    * `redpanda.wasm`: +4 metrics
  * Debug bundles
    * `redpanda.debug_bundle`: +4 metrics

* Added new metrics under existing default metrics groups:
  * `redpanda.application`: +1 metric
  * `redpanda.cluster`: +5 metrics
  * `redpanda.rpc`: +2 metrics
  * `redpanda.kafka`: +8 metrics
  * `redpanda.raft`: +5 metrics
  * `redpanda.storage`: +2 metrics

* Added new metrics under existing additional metrics groups:
  * `redpanda.cloud`: +27 metrics
  * `redpanda.pandaproxy`: +3 metrics
  * `redpanda.schemaregistry`: +7 metrics

***Fixed***:

* Typo: `redpanda.schema_registry_latency_seconds` is now `redpanda.schema_registry.latency_seconds`
* Typo: `redpanda_cloud_client_dowload_backoff` is now `cloud.client_download_backoff`

## 2.1.1 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [2829](@https://github.com/DataDog/integrations-extras/pull/2829)

## 2.1.0 / 2025-06-18

***Added***:

* Added support for consumer group lag metrics. See [CORE-8915](https://github.com/redpanda-data/redpanda/pull/25216). 

## 2.0.0 / 2023-08-21

***Added***:

* Moved to support Public Metrics endpoint from Redpanda and Redpanda Cloud. See [#1864](https://github.com/DataDog/integrations-extras/pull/1864).

## 1.1.1 / 2023-04-28

***Fixed***:

* Remove the use_latest_spec option from the config file ([#1835](https://github.com/DataDog/integrations-extras/pull/1835))

## 1.1.0 / 2022-03-24

***Added***:

* Add RP consumer group offset ([#1237](https://github.com/DataDog/integrations-extras/pull/1237). Thanks [bpraseed](https://github.com/bpraseed))
* Add `pyproject.toml` file ([#1185](https://github.com/DataDog/integrations-extras/pull/1185))
* Add curated_metric column to metadata.csv files ([#1209](https://github.com/DataDog/integrations-extras/pull/1209))

***Fixed***:

* Update conf.yaml.example files ([#1147](https://github.com/DataDog/integrations-extras/pull/1147))

## 1.0.0 / 2021-11-10

***Added***:

* Add Redpanda integration ([#1020](https://github.com/DataDog/integrations-extras/pull/1020))
