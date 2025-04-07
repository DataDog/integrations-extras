# CHANGELOG - redpanda

## 3.0.0 / 2025-03-20

***Removed***:

* Removed kafka.group_offset from default metrics.

## 2.1.0 / 2025-03-20

***Added***:

* Added metrics for consumer group lag.

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
