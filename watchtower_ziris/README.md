# Broadcom WatchTower z/IRIS

## Overview

Broadcom's WatchTower platform provides a comprehensive picture of mainframe health and performance. With its integrated real-time information streaming (z/IRIS), teams can anticipate failures based on past patterns, prevent small issues from becoming outages, and proactively manage z/OS operations.

This WatchTower z/IRIS integration collects metrics, logs, and traces via OpenTelemetry, and includes out-of-the-box content for seamless observability in Datadog:
- Monitor z/OS systems and applications using WatchTower's curated and customizable dashboards.
- Enable alerts on resource contention and application anomalies with WatchTower's recommended mainframe monitors.
- Enrich mainframe logs using the included log pipeline for easier analysis and correlation.

## Setup

### Prerequisite

Verify that WatchTower z/IRIS is installed and running. Refer to the WatchTower z/IRIS Installation documentation on the [TechDocs Portal][1] for more information about installing z/IRIS in your environment.

### Installation

1. **Configure the OpenTelemetry Collector**

   - Configure the OTLP receiver
   
   WatchTower z/IRIS can export telemetry over HTTP or gRPC. Refer to the  z/IRIS IronTap configuration to verify the appropriate receiver is configured.
   
   - Add a Transform Processor

   Use the OpenTelemetry Transform Processor to prefix all OpenTelemetry-based metrics streamed from z/IRIS with `ziris.`:

   ```json
   processors:
     transform/datadog:
        metric_statements:
           - context: metric
             statements:
               - set(metric.name,Concat(["ziris", metric.name], ".")) where HasPrefix(metric.name, "zos.")
               - set(metric.name,Concat(["ziris", metric.name], ".")) where HasPrefix(metric.name, "irontap.")
   ```

2. [Configure the Datadog Exporter and Connector][2]

   Follow Datadog's documentation to add the Datadog exporter to your collector configuration and provide your API key.
   Add the processor transform/datadog to the relevant pipelines exporting signals to your Datadog tenant.

3. Launch the collector and verify in Datadog that the renamed metrics (`ziris.*`) are appearing in the [Metrics Explorer][3] and verify that mainframe traces and spans are streaming.

4. In Datadog, open the WatchTower z/IRIS integration tile and click **Install**.

   Dashboards will be cloned into your organization, and the monitors will be available on the [Monitor Templates][4] page.



## Uninstallation

1. Stop the OpenTelemetry Collector or disable the Datadog Exporter.
2. In Datadog, open the WatchTower z/IRIS integration tile and click **Uninstall**.

## Support

Need help? Contact Broadcom by visiting [support.broadcom.com][5] and creating a support case for WatchTower z/IRIS.


[1]: https://techdocs.broadcom.com/
[2]: https://docs.datadoghq.com/opentelemetry/setup/collector_exporter/install/#2---configure-the-datadog-exporter-and-connector
[3]: https://app.datadoghq.com/metric/explorer
[4]: https://app.datadoghq.com/monitors/templates
[5]: https://support.broadcom.com/