# Agent Check: Unifi Console

## Overview

This check monitors [Unifi Console][1] through the Datadog Agent.

## Setup

The Unifi check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Unifi check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   sudo -u dd-agent -- datadog-agent integration install -t datadog-unifi_console==1.2.0
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `unifi_console.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Unifi Console performance data. See the [sample unifi_console.d/conf.yaml][11] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `unifi_console` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The Unifi Console integration does not include any events.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration.


## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://ui.com/consoles
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/unifi_console/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/unifi_console/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[11]: https://github.com/DataDog/integrations-extras/blob/master/unifi_console/datadog_checks/unifi_console/data/conf.yaml.example