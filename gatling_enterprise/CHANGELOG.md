# CHANGELOG - Gatling Enterprise

## 1.2.0 / 2025-09-09

_**Fixed**_:

Units changed from second to millisecond for metrics:
* gatling_enterprise.response.response_time.max 
* gatling_enterprise.response.response_time.min 
* gatling_enterprise.response.response_time.p95 
* gatling_enterprise.response.response_time.p99 
* gatling_enterprise.response.response_time.p999
* gatling_enterprise.response.tcp.connect_time.min
* gatling_enterprise.response.tcp.connect_time.max
* gatling_enterprise.response.tcp.connect_time.p95
* gatling_enterprise.response.tcp.connect_time.p99
* gatling_enterprise.response.tcp.connect_time.p999
* gatling_enterprise.response.tls.handshake_time.min
* gatling_enterprise.response.tls.handshake_time.max
* gatling_enterprise.response.tls.handshake_time.p95
* gatling_enterprise.response.tls.handshake_time.p99

## 1.1.0 / 2025-07-03

_**Added**_:
* TCP metrics (open, close, connect time)
* TLS metrics (count, handshake time)
* Requests and responses bandwidth usage in bits
* Response code

## 1.0.0 / 2025-05-27

_**Added**_:

* Initial Release
