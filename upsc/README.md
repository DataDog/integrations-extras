# UPSC Stats Collector Integration

## Overview

Get metrics from UPSD service through UPSC in real time to:

- Visualize and monitor UPS battery health and states
- Be notified about UPS failovers and events.

## Setup

The UPSC check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the UPSC check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-upsc==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `upsc.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your UPSC [metrics](#metrics). See the [sample upsc.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8]

## Validation

Run the [Agent's status subcommand][9] and look for `upsc` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Events

The UPSC check does not include any events.

### Service Checks

The UPSC check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][11].

[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/upsc/datadog_checks/upsc/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/upsc/metadata.csv
[11]: http://docs.datadoghq.com/help
