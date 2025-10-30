# Broadcom WatchTower z/IRIS

## Overview

Reduce your mean time to restore critical business services and improve service availability and reliability for core business applications with WatchTower's Real-Time OpenTelemetry Streaming capability (referred to as z/IRIS). WatchTower is a Broadcom Mainframe Software Product that provides a comprehensive picture of mainframe health, allowing you to anticipate failures based on past patterns, prevent small issues from becoming outages, and proactively manage your operations.  Each WatchTower capability can be used in silo or integrated with other capabilities to significantly broaden the range of contextual insights. 

Installing this WatchTower z/IRIS integration delivers a quick and easy out of the box experience for observability in Datadog:
- Monitor your z/OS system and applications using WatchTower's curated and customizable dashboards.
- Enable alerts on resource contention and application anomalies with WatchTowers recommended mainframe monitors.
- Continuously improve observability practices with access to all future Datadog resources created by WatchTower z/IRIS.

## Setup

**Prerequisite**
Verify that WatchTower z/IRIS is installed and running. Refer to the WatchTower z/IRIS Installation documentation on techdocs.broadcom.com for more information about installing z/IRIS in your environment. 

**Complete OpenTelemetry Collector Configuration**
- Configure the OTLP receiver \
   WatchTower z/IRIS can export telemetry over HTTP or gRPC. Refer to the  z/IRIS IronTap configuration to verify the appropriate receiver is configured.
- Add the Transform Processor \
   Add the prefix "ziris." to all opentelemetry basesd metrics streamed from  z/IRIS.
```json
transform/datadog:
   metric_statements:
      - context: metric
        statements:
          - set(name,concat("ziris.", name")) where starts_with((name, "zos.")
          - set(name,concat("ziris.", name")) where starts_with((name, "irontap.")

```
- Verify the Datadog Exporter and Connector are setup correctly\
   Follow Datadog's documentation to setup the Datadog Exporter and Connector for OpenTelemetry integration. 
- Starting the OpenTelemetry Collector\
    Verify that z/IRIS metrics is streaming with the correct prefix to Datadog.
- Install the out-of-the-box WatchTower z/IRIS Dashboards\
  All Dashobards can be copied and edited to meet your operational requirements.
- Install the out-of-the-box WatchTower z/IRIS Monitors\
   z/IRIS Monitors can be enabled to accelerate mean-time-to-restore.



## Uninstallation

**Mainframe: z/IRIS Client or zArchitecture Bridge (ZAB)** 

1. Identify if z/IRIS Client or ZAB is used to stream mainframe operational data for z/IRIS.
2. If the z/IRIS Client is implemented: Stop the z/IRIS Client
3. If ZAB is implemented: Remove subscriptions specific to the z/IRIS installation
2. Follow in-house procedures to remove SMP/E or z/OSMF installed software

_Note: ZAB can stream operational data for multiple Broadcom products and care should be taken to remove subscriptions that were unique to z/IRIS processing only. _

**Container: z/IRIS IronTap**

Using the commands applicable to your container engine:
1. Stop all IronTap containers
2. Remove all IronTap containers.

## Support

Log onto [support.broadcom.com][1] and create a case for WatchTower z/IRIS


[1]: https://support.broadcom.com/