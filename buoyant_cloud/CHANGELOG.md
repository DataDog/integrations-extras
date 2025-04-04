# CHANGELOG - Buoyant Cloud

## 1.2.0 / 2024-09-03

***Changed***:

* Replaced `pod.container_memory_working_set_bytes.sum` with `pod.container_memory_working_set_bytes.max`, to avoid double-counting memory usage during container restarts.

## 1.1.0 / 2023-05-01

***Added***:

* Buoyant Cloud metrics sent to Datadog.

## 1.0.0 / 2022-12-20

***Added***:

* Buoyant Cloud events sent to Datadog.
