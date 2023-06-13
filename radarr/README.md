# Agent Check: Radarr

## Overview

This check monitors [Radarr][1].


## Setup

The Radarr check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent versions 7.21 or 6.21 or later, follow the instructions below to install the Radarr check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   sudo -u dd-agent -- datadog-agent integration install -t datadog-radarr==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `radarr.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Radarr performance data. See the [sample radarr.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][5].

### Validation

Run the [Agent's status subcommand][6] and look for `radarr` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

Radarr does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://radarr.video/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/radarr/datadog_checks/radarr/data/conf.yaml.example
[9]: https://docs.datadoghq.com/help/
[10]: https://github.com/DataDog/integrations-extras/blob/master/radarr/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/radarr/assets/service_checks.json
