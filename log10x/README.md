# log10x

## Overview

The 10x Engine is a log pipeline engine that runs inside the operator's own network, in
front of Datadog. It reads events from a log forwarder, groups them by message pattern,
and decides per pattern what to do next: forward the events unchanged, compact them, or
offload them to the account's own object storage, which a query reads back.

Because the decision is made per pattern, the engine counts what every pattern sends
before anything changes, and what it sends afterwards. This integration carries those
counters into Datadog: volume and bytes for everything the pipeline read, volume and bytes
for what it forwarded, and the encoded size of forwarded events when compaction is on.
Every counter carries the same tag set, so any of them can be sliced by message pattern,
service, severity level or Kubernetes container. Two further counters make the reduction
reversible on paper: what went to offload storage, and what a query brought back.

Use the out-of-the-box dashboard to compare bytes and events into the pipeline against
bytes and events out of it, and to rank patterns by the bytes they contribute.

Log events stay inside the operator's network: no log data reaches log10x. The Datadog
Agent reads these metrics from the engine's own endpoint; the engine makes no call to
Datadog.

## Setup

This integration runs in the Datadog Agent and reads the 10x Engine's Prometheus metrics
endpoint. It is a community integration and is not bundled with the Agent.

### Prerequisites

A running 10x Engine, installed as described in the
[10x install documentation](https://doc.log10x.com/install/). The engine starts under a
built-in evaluation licence: no account, no signup, no token and no outbound call, up to
ten nodes, for thirty days from process start. A purchased licence is an offline file that
the engine verifies locally.

A Datadog Agent, version 7 or later, with network access to the engine's metrics port.

### Installation

#### 10x Engine

1. In the app configuration file, under **Select Metric Outputs**, uncomment the line
   `- run/output/metric/prometheus/scrape`. It can also be passed at launch as
   `@run/output/metric/prometheus/scrape`.
2. Restart the pipeline. At startup the engine prints
   `Publishing TenXSummary metrics to Prometheus scrape on port: 9100`. To change the
   port, edit `port` in `run/output/metric/prometheus/scrape/config.yaml`.

#### Datadog Agent

1. Install the integration on the Agent host:
   `datadog-agent integration install -t datadog-log10x==1.0.0`. See
   [Use Community Integrations](https://docs.datadoghq.com/agent/guide/use-community-integrations/)
   for the container and Kubernetes forms of this step.
2. Create `conf.d/log10x.d/conf.yaml` from the packaged `conf.yaml.example` and set
   `openmetrics_endpoint` to the engine's address, for example
   `http://localhost:9100/metrics`. On Kubernetes, use
   [Autodiscovery](https://docs.datadoghq.com/containers/kubernetes/integrations/)
   annotations on the engine's pod instead.
3. Restart the Agent.
4. Run `datadog-agent status` and confirm `log10x` appears under **Running Checks**.

## Uninstallation

1. Remove `conf.d/log10x.d/conf.yaml` and run
   `datadog-agent integration remove datadog-log10x`, then restart the Agent.
2. Comment the `- run/output/metric/prometheus/scrape` line back out of the engine's app
   configuration file and restart the pipeline.
3. Use the [delete dashboard](https://docs.datadoghq.com/dashboards/#delete-dashboard)
   option in the dashboard settings to remove the 10x dashboard.

## Data Collected

### Metrics

See [metadata.csv](metadata.csv) for the list of metrics this integration submits. They
fall into four families:

- Everything the pipeline read, in events and in bytes.
- What the pipeline forwarded, in events and in bytes, plus the encoded size when
  compaction is on.
- What was written to offload storage, in events and in bytes.
- What a retrieval query returned, in events and in bytes.

### Events

This integration does not submit events.

### Service Checks

**log10x.openmetrics.health**: Returns `CRITICAL` if the Agent cannot reach the engine's
metrics endpoint, otherwise `OK`.

## Troubleshooting

**The check is not listed in `datadog-agent status`.** The integration is not bundled with
the Agent; confirm the install step completed and that `conf.d/log10x.d/conf.yaml` exists.

**`log10x.openmetrics.health` is `CRITICAL`.** The Agent cannot reach the endpoint. Check
the engine log for `Publishing TenXSummary metrics to Prometheus scrape on port`, and that
the port in `conf.yaml` matches it.

**Series arrive with no `message_pattern` tag.** Pattern enrichment comes from the
`run/initialize/message` module. Confirm it is included in the engine's app configuration.

## Support

Contact [log10x support](mailto:support@log10x.com).
