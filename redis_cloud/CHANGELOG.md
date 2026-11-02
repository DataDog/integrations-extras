# CHANGELOG - Redis Cloud

## 1.1.2 / 2026-09-17

***Fixed***

* Fix a `ValueError` raised at check initialization against `datadog-checks-base` 37.39.0 or later. The check's `get_default_config` method shadowed the `OpenMetricsBaseCheckV2` method of the same name and has been renamed to `get_default_metrics` [#3127](https://github.com/DataDog/integrations-extras/pull/3127)
* Regenerate `conf.yaml.example` and config models with the current `ddev` codegen [#3127](https://github.com/DataDog/integrations-extras/pull/3127)

## 1.1.1 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [#2829](https://github.com/DataDog/integrations-extras/pull/2829)

## 1.1.0 / 2024-11-04

***Changed***:

* Removed redis_cloud.yaml file
* Replaced file descriptor panel with buffer memory panel in Redis Cloud Networking dashboard

***Added***:

* Added Proxy Dashboard
* Added Proxy-Threads Dashboard
* Added Active-Active Dashboard

## 1.0.0 / 2024-09-26

***Added***:

* Initial Release
