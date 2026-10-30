# log10x

## Overview

The 10x Engine is a log pipeline engine that runs inside the operator's own network, in
front of Datadog. It names each log line by its most likely source statement, the
pattern, or by the line's own known words when no source matches. The Receiver counts each
pattern per container against a limit: one threshold and one action for each service the
operator configures, and a fleet default for every other service. Above the limit the
excess takes the action: `tier_down` marks it for a Flex Logs index, where it still reaches
Datadog and stays searchable; `offload` sends it to the account's own object storage,
which the Retriever, a separate 10x deployment, indexes and reads back on a query.
Compaction does not apply to Datadog. Every forwarded event carries the route it took
in its `routeState` field and, when configured, the pattern hash in `tenx_hash`. Datadog
lowercases tag keys, so on the metrics the route appears as `routestate`.

Because every line is named by its pattern, the engine counts what every pattern sends
before anything changes, and what it sends afterwards. This integration carries those
counters into Datadog: volume and bytes for everything the pipeline read, and volume and
bytes for what it forwarded.
Every counter carries the same tag set, so any of them can be sliced by message pattern,
service, severity level, route (`routestate`, when the rate receiver runs), or Kubernetes
container. Four further counters, emitted by the
Retriever rather than by the pipeline, record what went to offload storage and what a
retrieval query returned, in events and in bytes.

Use the out-of-the-box dashboard to compare bytes and events into the pipeline against
bytes and events out of it, and to rank patterns by the bytes they contribute.

The 10x Engine runs inside the operator's network. No log data reaches log10x. The Datadog
Agent scrapes the Prometheus endpoint on the engine, and on the Retriever where one is
deployed, and submits these metrics to Datadog.

## Setup

This integration runs in the Datadog Agent and reads the 10x Engine's Prometheus metrics
endpoint, and the Retriever's where one is deployed. Community integrations are not
bundled with the Agent, so install this integration separately.

### Prerequisites

- A running 10x Engine, installed as described in the
  [10x install documentation](https://doc.log10x.com/install/). The engine starts under a
  built-in evaluation license, up to 10 nodes for 30 days from process start; its terms
  are in the [operations documentation](https://doc.log10x.com/security/operations/). A
  purchased license is an offline file that the engine verifies locally.
- A Datadog Agent, version 7 or later, with network access to the engine's metrics port.

### Installation

#### 10x Engine

1. In the app configuration file, under **Select Metric Outputs**, uncomment the line
   `- run/output/metric/prometheus/scrape`. You can also pass the line at launch as
   `@run/output/metric/prometheus/scrape`.
2. Restart the pipeline. At startup, the engine prints
   `Publishing TenXSummary metrics to Prometheus`, followed by the port, which is `9100` by
   default. To change it, edit `port` in `run/output/metric/prometheus/scrape/config.yaml`.

#### Datadog Agent

Run the following command on the Agent host:

```shell
datadog-agent integration install -t datadog-log10x==1.0.0
```

For containerized and Kubernetes environments, see [Use Community and Marketplace Integrations](https://docs.datadoghq.com/agent/guide/use-community-integrations/).

### Configuration

1. Create `conf.d/log10x.d/conf.yaml` from the packaged `conf.yaml.example` and set
   `openmetrics_endpoint` to the engine's address, for example
   `http://localhost:9100/metrics`. On Kubernetes, use
   [Autodiscovery](https://docs.datadoghq.com/containers/kubernetes/integrations/#configuration)
   annotations on the engine's pod instead.
2. For the offload and retrieval counters, add a second instance pointing at the
   Retriever's own endpoint, on the same default port, for example
   `http://<retriever-host>:9100/metrics`. Without this instance, the dashboard's
   Offload storage group stays empty. Configure the instance as follows:
   - Set `ignore_connection_errors: true` and `enable_health_service_check: false`. The
     Retriever opens its port only while an index or query run is in flight. Without
     these settings, Datadog reports the closed port between runs as a failure.
   - Optionally, set a shorter `min_collection_interval`, such as `5`, to increase the
     chance of collecting metrics during a run.
   - On Kubernetes, use the same Autodiscovery annotation on the Retriever's index,
     query, and stream pods.

   **Note**: On Lambda, the Retriever has no endpoint for the Agent to scrape, so the
   offload and retrieval metrics are not available.
3. Restart the Agent.

### Validation

Run `datadog-agent status` and confirm `log10x` appears under **Running Checks**.

## Uninstallation

1. Remove `conf.d/log10x.d/conf.yaml` and run
   `datadog-agent integration remove datadog-log10x`, then restart the Agent.
2. Comment the `- run/output/metric/prometheus/scrape` line back out of the engine's app
   configuration file and restart the pipeline.
3. Use the [delete dashboard](https://docs.datadoghq.com/dashboards/configure/#delete-dashboard)
   option in the dashboard settings to remove the 10x dashboard.

## Data Collected

### Metrics

See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/log10x/metadata.csv) for the full list with types and units.

| Metric | Emitted by | Counts |
|---|---|---|
| `log10x.check.up` | The check | One on every run |
| `log10x.events.read.count`, `log10x.bytes.read.count` | Pipeline | Everything the pipeline read |
| `log10x.events.forwarded.count`, `log10x.bytes.forwarded.count` | Pipeline | Every event returned to the forwarder, on any route. Split by `routestate` to see what went to Standard Indexing (`pass`), Flex Logs (`tier_down`), and storage (`offload`) |
| `log10x.events.offloaded.count`, `log10x.bytes.offloaded.count` | Retriever index | What was written to offload storage |
| `log10x.events.retrieved.count`, `log10x.bytes.retrieved.count` | Retriever query | What a retrieval query returned |

The last four come from the Retriever, which runs as its own deployment, so the Agent needs
a second instance pointing at it: on Kubernetes, an Autodiscovery annotation on the index,
query, and stream pods. On Lambda, the Retriever has no endpoint for the Agent to scrape, so
those four metrics do not arrive through this check.

### Events

This integration does not submit events.

### Service Checks

**log10x.openmetrics.health**: Returns `CRITICAL` if the Agent cannot reach the engine's
metrics endpoint, otherwise `OK`.

## Troubleshooting

- **The check is not listed in `datadog-agent status`.** The integration is not bundled
  with the Agent; confirm the install step completed and that `conf.d/log10x.d/conf.yaml`
  exists.
- **`log10x.openmetrics.health` is `CRITICAL`.** The Agent cannot reach the endpoint. Check
  the engine log for `Publishing TenXSummary metrics to Prometheus`, and that the port it
  names matches the one in `conf.yaml`.
- **Series arrive with no `message_pattern` tag.** Pattern enrichment comes from the
  `run/initialize/message` module. Confirm it is included in the engine's app
  configuration.

## Support

Contact [log10x's support team](mailto:support@log10x.com).
