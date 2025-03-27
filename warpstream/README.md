
## Overview

WarpStream is an Apache Kafka® compatible data streaming platform built directly on top of object storage: no inter-AZ networking costs, no disks to manage, and infinitely scalable, all within your VPC.

The Datadog Agent collects many metrics from Warpstream.

Metrics are sent directly from the [WarpStream Agent][2] to Datadog's [DogStatsD][3].

## Setup

### Installation

All steps below are needed for the Warpstream integration to work properly. Before you begin, [install the Datadog Agent][3] version `>=6.17` or `>=7.17`.

### Configuration

There are two parts of the Warpstream integration:

- The Datadog Agent portion, which makes requests to a provided endpoint for Warpstream agent to report whether it can connect and is healthy.
- The Warpstream StatsD portion, where Warpstream Agent can be configured to send metrics to the Datadog Agent.

The Warpstream integration's [metrics](#metrics) come from both the Agent and StatsD portions.

<!-- xxx tabs xxx -->
<!-- xxx tab "Host" xxx -->

#### Host

##### Configure Datadog Agent Warpstream integration

Configure the Warpstream check included in the [Datadog Agent][4] package to collect health metrics and service checks. This can be done by editing the `url` within the `warpstream.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory, to start collecting your Warpstream service checks. See the [sample warpstream.d/conf.yaml][5] for all available configuration options.

Ensure that `url` matches your Warspstream Agent HTTP server (port 8080 by default).

##### Connect Warpstream Agent to DogStatsD

Start the agent with the flag `-enableDatadogMetrics` or set the environment variable `WARPSTREAM_ENABLE_DATADOG_METRICS` to `true`.

##### Restart Datadog Agent and Warpstream

1. [Restart the Agent][6].
2. Restart Warpstream agent to start sending your Warpstream metrics to the Agent DogStatsD endpoint.


## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

## Troubleshooting

Need help? Contact [Datadog support][8].

[1]: https://www.warpstream.com/
[2]: https://docs.warpstream.com/warpstream/byoc/deploy
[3]: https://docs.datadoghq.com/developers/dogstatsd/
[4]: https://app.datadoghq.com/account/settings/agent/latest
[5]: https://github.com/DataDog/integrations-extras/blob/master/warpstream/datadog_checks/warpstream/data/conf.yaml.example
[6]: https://github.com/DataDog/integrations-extras/blob/master/warpstream/metadata.csv
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[8]: https://docs.datadoghq.com/help/

