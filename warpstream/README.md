# WarpStream

## Overview

WarpStream is a data streaming platform compatible with Apache Kafka®, designed to run directly on object storage. This integration provides visibility into WarpStream agent performance by exposing key metrics, helping users monitor both health and performance.

## Setup

### Installation

1.  [Download and launch the Datadog Agent][1].
2.  Manually install the WarpStream integration. See [Use Community Integrations][2] for more details based on the environment.

### Configuration

Complete the following steps to set up the WarpStream integration.

The WarpStream integration has two components:

-   The **Datadog Agent** component, which makes requests to an endpoint to check whether WarpStream can connect and is healthy.

-   The **WarpStream StatsD** component, which you configure to send metrics to the Datadog Agent.

The WarpStream integration's [metrics][3] come from both the Agent and StatsD portions.

#### Configure the Datadog Agent WarpStream integration

Edit the `url` in `warpstream.d/conf.yaml`, in the `conf.d/` folder at the root of your Agent's configuration directory. See the [sample `warpstream.d/conf.yaml`][4] for all available configuration options.

The `url` value must match your WarpStream Agent HTTP server (port 8080 by default).

##### Connect WarpStream Agent to DogStatsD

Start the WarpStream Agent with the flag `-enableDatadogMetrics` or set the environment variable `WARPSTREAM_ENABLE_DATADOG_METRICS` to `true`.

##### Restart Datadog Agent and WarpStream

1. [Restart the Agent][5].

2. Restart the WarpStream Agent to start sending your WarpStream metrics to the Agent DogStatsD endpoint.

## Uninstallation

1. Remove the integration yaml config file and restart the Datadog Agent.

2. Unset the `-enableDatadogMetrics` flag and restart the WarpStream Agent.

## Support

Need help? Contact us through the following channels:
- Slack: https://console.warpstream.com/socials/slack
- Discord: https://discord.com/invite/rSFx8vqjVY



[1]: https://docs.datadoghq.com/containers/kubernetes/log/
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://github.com/warpstreamlabs/integrations-extras/tree/epot/tier/warpstream#metrics
[4]: https://github.com/DataDog/integrations-extras/blob/master/warpstream/datadog_checks/warpstream/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/configuration/agent-commands/#start-stop-and-restart-the-agent