# Agent Check: Speedtest

## Overview

This check monitors [Speedtest][1] through the Datadog Agent.

## Setup

The Speedtest check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Speedtest check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-speedtest==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

**Note**: For all hosts, you need to also install the [Speedtest CLI][1] and accept the agreement as the Datadog Agent user prior to use, for example: `sudo -u dd-agent speedtest`.

### Configuration

1. Edit the `speedtest.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Speedtest performance data. See the [sample speedtest.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `speedtest` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Events

Speedtest does not include any events.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].


[1]: https://www.speedtest.net/apps/cli
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://github.com/DataDog/integrations-extras/blob/master/speedtest/datadog_checks/speedtest/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[11]: https://github.com/DataDog/integrations-extras/blob/master/speedtest/metadata.csv
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/speedtest/assets/service_checks.json
