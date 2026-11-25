# CHANGELOG - Modal

## 1.10.0 / 2026-11-25

***Added***:

* Queued and running request metrics for Servers
* Input queue time metric, which Servers that queue requests also send
* Queue outcome tag on input event metrics

## 1.9.0 / 2026-11-24

***Added***:

* Network egress and ingress bytes metrics
* GPU clock metric
* Sandbox ID tag on container metrics from Modal Sandboxes

## 1.8.1 / 2026-10-13

***Changed***:

* Show p50 and p90 input execution time on the Modal dashboard instead of the average

## 1.8.0 / 2026-09-10

***Added***:

* GPU count metric
* GPU billing type tag on container resource metrics

## 1.7.0 / 2026-09-04

***Added***:

* CPU requested and memory requested

## 1.6.0 / 2026-05-14

***Added***:

* GPU power, power utilization, and temperature metrics

## 1.5.0 / 2025-11-06

***Added***:

* Container running metric

## 1.4.0 / 2025-09-21

***Added***:

* Container termination metrics
* New memory metric which includes units, and reports in bytes

## 1.3.0 / 2025-05-12

***Added***:

* Input metrics

## 1.2.0 / 2024-11-27

***Added***:

* Container metrics

## 1.1.0 / 2024-07-09

***Added***:

* Modal now publishes app logs to Datadog.

## 1.0.0 / 2024-02-29

***Added***:

* Initial Release
