# WarpStream

## Overview

WarpStream is a data streaming platform compatible with Apache Kafka®, designed to run directly on object storage. This integration provides visibility into WarpStream agent performance by exposing key metrics, helping users monitor both health and performance.

## Setup

### Installation

[Install the Datadog Agent][1] version `>=6.17` or `>=7.17`.

### Configuration

Complete all of the following steps to ensure the WarpStream integration works properly.

There are two parts of the WarpStream integration:

-   The **Datadog Agent** portion, which makes requests to a provided endpoint for the WarpStream agent to report whether it can connect and is healthy.

-   The **WarpStream StatsD** portion, where WarpStream Agent can be configured to send metrics to the Datadog Agent.

The WarpStream integration's [metrics][2] come from both the Agent and StatsD portions.

##### Configure Datadog Agent WarpStream integration

Configure the WarpStream check included in the [Datadog Agent][3] package to collect health metrics and service checks. This can be done by editing the `url` within the `warpstream.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory, to start collecting your WarpStream service checks. See the [sample warpstream.d/conf.yaml][4] for all available configuration options.

Ensure that `url` matches your WarpStream Agent HTTP server (port 8080 by default).

##### Connect WarpStream Agent to DogStatsD

Start the agent with the flag `-enableDatadogMetrics` or set the environment variable `WARPSTREAM_ENABLE_DATADOG_METRICS` to `true`.

##### Restart Datadog Agent and WarpStream

1. [Restart the Agent][5].

2. Restart the WarpStream agent to start sending your WarpStream metrics to the Agent DogStatsD endpoint.

## Uninstallation

1. Remove the integration yaml config file and restart the Datadog agent
2. Unset the `-enableDatadogMetrics` flag and restart the WarpStream agent

## Support

Need help? Contact us through the following channels:
- Slack: https://console.warpstream.com/socials/slack
- Discord: https://discord.com/invite/rSFx8vqjVY



[1]: https://docs.datadoghq.com/developers/dogstatsd/
[2]: https://github.com/warpstreamlabs/integrations-extras/tree/epot/tier/warpstream#metrics
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://github.com/DataDog/integrations-extras/blob/master/warpstream/datadog_checks/warpstream/data/conf.yaml.example
[5]: https://github.com/DataDog/integrations-extras/blob/master/warpstream/metadata.csv