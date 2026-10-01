# log10x

## Overview

The 10x Engine is a log pipeline engine that runs inside the operator's own network, in
front of Datadog. It reads events from a log forwarder, groups them by message pattern,
and decides per pattern what to do next: forward the events unchanged, compact them, or
offload them to the account's own object storage, which the Retriever, a separate 10x
deployment, indexes and reads back on a query.

Because the decision is made per pattern, the engine counts what every pattern sends
before anything changes, and what it sends afterwards. This integration carries those
counters into Datadog: volume and bytes for everything the pipeline read, volume and bytes
for what it forwarded, and the encoded size of forwarded events when compaction is on.
Every counter carries the same tag set, so any of them can be sliced by message pattern,
service, severity level, or Kubernetes container. Four further counters, emitted by the
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
bundled with the Agent, so it is installed separately.

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
   `- run/output/metric/prometheus/scrape`. It can also be passed at launch as
   `@run/output/metric/prometheus/scrape`.
2. Restart the pipeline. At startup, the engine prints
   `Publishing TenXSummary metrics to Prometheus`, followed by the port, which is `9100` by
   default. To change it, edit `port` in `run/output/metric/prometheus/scrape/config.yaml`.

#### Datadog Agent

Install the integration on the Agent host:
`datadog-agent integration install -t datadog-log10x==1.0.0`. See
[Use Community and Marketplace Integrations](https://docs.datadoghq.com/agent/guide/use-community-integrations/)
for the container and Kubernetes forms of this step.

### Configuration

1. Create `conf.d/log10x.d/conf.yaml` from the packaged `conf.yaml.example` and set
   `openmetrics_endpoint` to the engine's address, for example
   `http://localhost:9100/metrics`. On Kubernetes, use
   [Autodiscovery](https://docs.datadoghq.com/containers/kubernetes/integrations/#configuration)
   annotations on the engine's pod instead.
2. For the offload and retrieval counters, add a second instance pointing at the
   Retriever's own endpoint, on the same default port, for example
   `http://<retriever-host>:9100/metrics`. The Retriever opens that port only while an
   index or a query run is in flight and closes it when the run ends, so set
   `ignore_connection_errors: true` and `enable_health_service_check: false` on that
   instance, otherwise the closed port between runs is reported as a failure. A shorter
   `min_collection_interval`, for example 5, gives the Agent more chances to land inside
   a run. On Kubernetes, use the same
   Autodiscovery annotation on the Retriever's index, query, and stream pods. On Lambda,
   the Retriever has no endpoint for the Agent to scrape, so those four metrics do not
   arrive. Without this instance, the dashboard's Offload storage group stays empty.
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

## Data collected

### Metrics

See [metadata.csv](metadata.csv) for the full list with types and units.

| Metric | Emitted by | Counts |
|---|---|---|
| `log10x.check.up` | The check | One on every run |
| `log10x.events.read.count`, `log10x.bytes.read.count` | Pipeline | Everything the pipeline read |
| `log10x.events.forwarded.count`, `log10x.bytes.forwarded.count` | Pipeline | What it forwarded downstream |
| `log10x.bytes.encoded.count` | Pipeline | Encoded size of forwarded events when compaction is on |
| `log10x.events.offloaded.count`, `log10x.bytes.offloaded.count` | Retriever index | What was written to offload storage |
| `log10x.events.retrieved.count`, `log10x.bytes.retrieved.count` | Retriever query | What a retrieval query returned |

The last four come from the Retriever, which runs as its own deployment, so the Agent needs
a second instance pointing at it: on Kubernetes, an Autodiscovery annotation on the index,
query, and stream pods. On Lambda, the Retriever has no endpoint for the Agent to scrape, so
those four metrics do not arrive through this check.

### Events

This integration does not submit events.

### Service checks

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
