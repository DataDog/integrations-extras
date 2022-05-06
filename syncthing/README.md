# Agent Check: Syncthing

## Overview

Syncthing synchronizes files between two or more computers in real time. This integration allows you to monitor [Syncthing][1] using Datadog.

## Setup

The Syncthing check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Syncthing check on your host. See [Use Community Integrations][3] to install the Syncthing check with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-syncthing==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `syncthing.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Syncthing [metrics](#metrics). See the [sample syncthing.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

### Validation

Run the [Agent's status subcommand][10] and look for `syncthing` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Events

Syncthing does not include any events.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].


[1]: https://syncthing.net/ 
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/syncthing/datadog_checks/syncthing/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/syncthing/metadata.csv
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/syncthing/assets/service_checks.json
