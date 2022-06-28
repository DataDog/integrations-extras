# Agent Check: Unifi Console

## Overview

This check monitors [Unifi Controller][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

To install the Unifi Console check on your host:


1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build unifi_console` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/unifi_console/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `unifi_console.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your unifi_console performance data. See the [sample unifi_console.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `unifi_console` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The Unifi Console integration does not include any events.

### Service Checks

The Unifi Console integration does not include any service checks.

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://ui.com/consoles
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-core/blob/master/unifi_console/datadog_checks/unifi_console/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-core/blob/master/unifi_console/metadata.csv
[8]: https://github.com/DataDog/integrations-core/blob/master/unifi_console/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
