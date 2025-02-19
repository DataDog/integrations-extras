# CHANGELOG - fiddler

## 4.0.0 / 2025-01-28

***Changed***:

* Migrated to v3 queries and metrics APIs ([#2592](https://github.com/DataDog/integrations-extras/pull/2592))
* Updated configuration/spec.yaml to make the integration more configurable ([#2592](https://github.com/DataDog/integrations-extras/pull/2592))
* Deprecated old metric names and the v1compat flag in configuration ([#2592](https://github.com/DataDog/integrations-extras/pull/2592))

***Added***:

* Introduced new metric names ([#2592](https://github.com/DataDog/integrations-extras/pull/2592))
* Added a new dashboard to support the new metric names ([#2592](https://github.com/DataDog/integrations-extras/pull/2592))

## 3.0.0 / 2024-03-06

***Changed***

* Changed metric name mapping for DI violations, and performance metric to ensure 23.7 to 23.5 compatibility

## 2.0.0 / 2024-01-16

***Changed***

* Changed to using faster v2 queries API.
* Changed metric name expected_callibration_error to expected_calibration_error
* Changed metric name callibrated_threshold to calibrated_threshold

## 1.0.0 / 2023-02-05

***Added***:

* Fiddler Datadog integration.
