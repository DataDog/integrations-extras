# CHANGELOG - Broadcom WatchTower z/IRIS

## 1.3.0 / 2025-10-30

_**New Features**_:

* Broadcom SYSVIEW customers can configure z/IRIS to  stream OpenTelemetry (OTel) JVM Garbage Collection metrics for enhanced monitoring and performance analysis. For more details, see [OpenTelemetry JVM Garbage Collection Metrics ](https://techdocs.broadcom.com/us/en/ca-mainframe-software/intelligent-operations/watchtower-platform-suite/1-2/reference/z-iris-telemetry/opentelemetry-metrics/opentelemetry-jvm-garbage-collection-metrics.html#_e440c267-53a0-4566-9bc7-896b5e3d0527_JVMGC).

_**Improvements**_:

*  service name granularity has been enhanced by extracting distinguishing precise service identification.

Unit of Work | Service Name
------|------
 z/OS Connect API | REST API Name 
CICS transaction | CICS Region Name

 Users can customize the service name in the OpenTelemetry Collector. For  For detailed steps to customize the service name , see the [z/IRIS OpenTelemetry Collector Configuration](https://techdocs.broadcom.com/us/en/ca-mainframe-software/intelligent-operations/watchtower-platform-suite/1-2/administrating/administrate-ziris/observability-with-opentelemetry/configure-opentelemetry-contrib-collector.html#configuring_opentelemetry_contrib_collector) page.

* z/IRIS IronTap added OTLP/HTTP support for all signal transmission. The existing gRPC transport protocol remains supported. The configuration option is described in the [Complete z/IRIS IronTap Configuration Tasks](https://techdocs.broadcom.com/us/en/ca-mainframe-software/intelligent-operations/watchtower-platform-suite/1-2/installing/install-z-iris/install-z-iris-irontap/configure-z-iris-irontap.html#concept.dita_configure_irontap_container_CTB) page.

 * A new configurable option is available to set the ERROR status on CICS  spans when exception conditions impact the reliability of transaction. See the CICS Transaction Error Reporting section in the [CICS Spans](https://techdocs.broadcom.com/us/en/ca-mainframe-software/intelligent-operations/watchtower-platform-suite/1-2/reference/z-iris-telemetry/spans/cics-spans.html#cics_spans_err) page for steps to configure the span error status.

* Log correlation has been enhanced. Logs are tagged with the trace context (trace_id and span_id), enabling a direct correlation between logs and spans from the same unit-of-work. If a span was not established the log entry will not contain any trace context.
