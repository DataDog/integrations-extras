# KurrentDB Integration

## Overview

[KurrentDB][1] (formerly EventStoreDB) is an event-native database. This integration collects:

* The Prometheus metrics that KurrentDB exposes on its `/metrics` endpoint
* Cluster membership, node role, projection, subscription, and queue metrics from KurrentDB's JSON HTTP API (`/gossip`, `/info`, `/projections/all-non-transient`, `/subscriptions`, and `/stats`)

With these you can:

* Monitor cluster health, including member liveness, commit positions, elections, and gossip latency
* Track reads, writes, gRPC calls, and queue latency
* Watch persistent subscription and projection progress
* Observe process, garbage collection, and system resource usage

**Note**: This integration replaces the deprecated `eventstore` integration. See [Migrating from the eventstore integration](#migrating-from-the-eventstore-integration).

## Setup

The KurrentDB check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the KurrentDB check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-kurrentdb==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `kurrentdb.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][5] to start collecting your KurrentDB [metrics](#metrics). At a minimum, set `openmetrics_endpoint`:

   ```yaml
   instances:
     - openmetrics_endpoint: http://localhost:2113/metrics
   ```

   By default, the check also collects metrics from the KurrentDB JSON API at the same host, for example `http://localhost:2113/gossip`. Use these options to change that:

   | Option      | Description                                                                                                                      |
   | ----------- | -------------------------------------------------------------------------------------------------------------------------------- |
   | `url`       | Base URL of the JSON API. Defaults to `openmetrics_endpoint` without the trailing `/metrics`.                                    |
   | `endpoints` | The JSON API endpoints to collect. Defaults to `/stats`, `/info`, `/projections/all-non-transient`, `/subscriptions`, `/gossip`. Set to `[]` to collect only the Prometheus metrics. |

   Endpoints that return a 404, such as `/projections/all-non-transient` when projections are disabled, are skipped. Authentication and TLS settings, such as `username`, `password`, and `tls_ca_cert`, apply to both the Prometheus and JSON API requests. See the [sample kurrentdb.d/conf.yaml][6] for all available configuration options.

2. [Restart the Agent][7].

#### Enabling metrics on KurrentDB

KurrentDB only emits the Prometheus metrics enabled in its `metricsconfig.json`, located in the installation directory. Enable the metrics you want to collect there. See the [KurrentDB metrics documentation][8] for the available options. The JSON API metrics do not depend on this file.

If you use the OpenTelemetry Collector to re-export KurrentDB metrics in Prometheus format, set `add_metric_suffixes` to `false` in its Prometheus exporter configuration so the metric names are unchanged.

### Validation

[Run the Agent's status subcommand][9] and look for `kurrentdb` under the Checks section.

### Migrating from the eventstore integration

The `eventstore` integration collected metrics from KurrentDB's JSON HTTP API. This integration collects the same metrics and adds the Prometheus metrics from `/metrics`.

* Metrics from the JSON API keep their names with the prefix changed from `eventstore.` to `kurrentdb.`. For example, `eventstore.cluster.member_alive` is now `kurrentdb.cluster.member_alive`, and `eventstore.es.queue.length` is now `kurrentdb.es.queue.length`.
* The Prometheus metrics are named `kurrentdb.<prometheus name without the kurrentdb_ prefix>`, for example `kurrentdb.proc_thread_count`. Some overlap with the JSON API metrics. For example, `kurrentdb.proc.mem` (JSON API) and `kurrentdb.proc_mem_bytes` (Prometheus) both report process memory.
* Set `openmetrics_endpoint` (for example, `http://localhost:2113/metrics`), which is now required. `url` and `endpoints` still work, and `endpoints` is optional and defaults to all five endpoints.
* The `json_path` and `name` options and the `metric_definitions` init config option are removed, because all metrics are collected. To drop metrics, use `exclude_metrics` (see [Metrics](#metrics)).
* The HTTP options are renamed: `user` is `username`, `ca_bundle` is `tls_ca_cert`, and `default_timeout` is `timeout`.
* The `name` and `instance` tags are replaced by an `endpoint` tag holding the URL that was queried. Other tags are unchanged, such as `projection`, `queue_name`, `group_name`, `event_stream_id`, `http_end_point_ip`, and `http_end_point_port`.
* The `eventstore.es.queue.avg_items_per_second`, `eventstore.es.queue.avg_processing_time`, `eventstore.es.queue.length`, and `eventstore.subscription.average_items_per_second` histograms are now gauges, because a single value is reported per check run.
* `eventstore.running_projections.*` was listed in the old metadata but never collected, so it is not included.
* The TCP metrics (`kurrentdb.tcp.*`) remain for compatibility, but KurrentDB removed the external TCP API in 24.2.0, so they report zero.
* KurrentDB 26.0 removed the queue busyness metric. Use `kurrentdb.es.queue.length` and `kurrentdb.queue_queueing_duration_max_seconds` instead.
* This check expects the `kurrentdb_` Prometheus metric prefix. If you set the meters in `metricsconfig.json` back to `EventStore.Core` and `EventStore.Projections.Core` to keep the old metric names, the Prometheus metrics are not collected. The JSON API metrics are unaffected.

## Compatibility

The check is compatible with KurrentDB 25.0 and later, the first release to use the `kurrentdb_` metric prefix.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

Counters from the Prometheus endpoint are submitted with a `.count` suffix, and histograms with `.bucket`, `.count`, and `.sum` suffixes. Prometheus labels, such as `cache`, `activity`, `projection`, and `event_stream_id`, are submitted as tags. The `otel_scope_name` and `otel_scope_version` labels are dropped.

The integration collects every metric that KurrentDB exposes on `/metrics`, including the ASP.NET Core, HTTP server, Kestrel, and messaging metrics that are not part of the KurrentDB metrics documentation. These can produce many time series, for example from `kurrentdb.http_server_request_duration_seconds` by route. To drop metrics you don't need, set `exclude_metrics` in your instance configuration:

```yaml
instances:
  - openmetrics_endpoint: http://localhost:2113/metrics
    exclude_metrics:
      - aspnetcore_.*
      - http_server_.*
```

Names in `exclude_metrics` are the Prometheus names without the `_total` suffix.

### Events

The KurrentDB check does not include any events.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration:

* `kurrentdb.openmetrics.health` reports whether the Prometheus endpoint can be scraped.
* `kurrentdb.api.can_connect` reports, per endpoint, whether a JSON API endpoint can be collected.

## Troubleshooting

Need help? Contact the [maintainer][12] of this integration.

[1]: https://www.kurrent.io/
[2]: /account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[6]: https://github.com/DataDog/integrations-extras/blob/master/kurrentdb/datadog_checks/kurrentdb/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[8]: https://docs.kurrent.io/server/latest/diagnostics/metrics.html
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/kurrentdb/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/kurrentdb/assets/service_checks.json
[12]: https://github.com/DataDog/integrations-extras/blob/master/kurrentdb/manifest.json
