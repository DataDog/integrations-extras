# Agent Check: Neutrona

## Overview

This check monitors [Neutrona][1] cloud connectivity services to:

- Azure (ExpressRoute)

## Setup

The Neutrona check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Neutrona check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-neutrona==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `neutrona.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Neutrona [metrics](#metrics).
   See the [sample neutrona.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

### Validation

[Run the Agent's status subcommand][10] and look for `neutrona` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Service Checks

Neutrona does not include any service checks at this time.

### Events

Neutrona does not include any events at this time.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://telemetry.neutrona.com
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/neutrona/datadog_checks/neutrona/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-core/blob/master/neutrona/metadata.csv
[12]: https://docs.datadoghq.com/help/
