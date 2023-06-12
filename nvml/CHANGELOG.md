# CHANGELOG - nvml

## 1.0.7 / 2023-06-07

* [Fixed] fix(nvml): decode no longer needed. See [#1774](https://github.com/DataDog/integrations-extras/pull/1774). Thanks [cep21](https://github.com/cep21).

## 1.0.6

* Add compute_running_process metrics.

## 1.0.5

* Add fan speed to monitored metrics.

## 1.0.4

* Change monotonic_count to gauge for temperature. 

## 1.0.3

* Fix version.

## 1.0.2

* Add GPU temperature metric. 

## 1.0.1

* [FIXED] Make nvml check quieter on non-GPU hosts (https://github.com/DataDog/integrations-extras/pull/817)
