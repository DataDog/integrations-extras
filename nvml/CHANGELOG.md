# CHANGELOG - nvml

## 1.0.9 / 2023-10-31

* Fix the API call compatibility issue ([related issue](https://github.com/DataDog/integrations-extras/issues/2159)).

## 1.0.8 / 2023-08-14

* Upgrade grpcio dependency to solve some linux/arm64 build errors ([related issue](https://github.com/DataDog/integrations-extras/issues/1752)).

## 1.0.7 / 2023-06-07

***Fixed***:

* fix(nvml): decode no longer needed ([#1774](https://github.com/DataDog/integrations-extras/pull/1774). Thanks [cep21](https://github.com/cep21))

## 1.0.6

***Added***:

* Add compute_running_process metrics.

## 1.0.5

***Added***:

* Add fan speed to monitored metrics.

## 1.0.4

***Changed***:

* Change monotonic_count to gauge for temperature. 

## 1.0.3

***Fixed***:

* Fix version.

## 1.0.2

***Added***:

* Add GPU temperature metric. 

## 1.0.1

***Fixed***:

* Make nvml check quieter on non-GPU hosts (https://github.com/DataDog/integrations-extras/pull/817)
