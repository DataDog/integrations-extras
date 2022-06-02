# Agent Check: Netnology SD-WAN

## Overview

This check monitors SD-WAN controllers through the Datadog Agent using an SD-WAN platform provided by [Netnology][1]. The
check enables users to monitor the network health and performance of multiple SD-WAN controllers simultaneously. Collected
information can then be used for aggregated dashboarding and notifications on configured monitors/alerts.

Currently, only Cisco vManage devices are supported as SD-WAN controller targets.

## Setup

The Netnology SD-WAN integration is not included in the [Datadog Agent][2] package, so you need to install it manually.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the check on your host. See [Use Community Integrations][10] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ``` bash
   datadog-agent integration install -t nn_sdwan==1.0.0
   ```

2. Configure your integration similar to core [integrations][3].

### Configuration

1. Edit the `nn_sdwan.d/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Netnology SD-WAN performance data. See [sample nn_sdwan.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `nn_sdwan` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The Netnology SD-WAN integration does not include any events.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://netnology.io
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/getting_started/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/nn_sdwan/datadog_checks/nn_sdwan/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/nn_sdwan/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/nn_sdwan/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://docs.datadoghq.com/agent/guide/use-community-integrations/ 