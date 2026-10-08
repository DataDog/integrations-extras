# CHANGELOG - Redis Enterprise

## 1.1.4 / 2026-09-17

***Fixed***

* Fix a `ValueError` raised at check initialization against `datadog-checks-base` 37.39.0 or later. The check's `get_default_config` method shadowed the `OpenMetricsBaseCheckV2` method of the same name and has been renamed to `get_default_metrics` [#3127](https://github.com/DataDog/integrations-extras/pull/3127)
* Regenerate `conf.yaml.example` and config models with the current `ddev` codegen [#3127](https://github.com/DataDog/integrations-extras/pull/3127)

## 1.1.3 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [#2829](https://github.com/DataDog/integrations-extras/pull/2829)

## 1.1.2 / 2025-02-28

***Changed***:

* Update `tls_verify` handling in check code to ensure default is set to 'True'

## 1.1.1 / 2025-01-21

***Changed***:

* Represent used memory as a percentage in Shard and Database dashboards

## 1.1.0 / 2024-10-06

***Changed***:

* Renamed Replication as Active-Active

***Added***:

* Added Shard dashboard
* Added Proxy Threads dashboard

## 1.0.1 / 2024-08-09

***Changed***:

* Fixed issue with extra_metrics not being reported
* Updated configuration documentation

***Added***:

* Added Replication and Proxy Dashboards
* Added tests to check all additional metrics
* Added node_cert_expiration_seconds to Node metrics

## 1.0.0 / 2024-05-02

***Added***:

* Initial Release

