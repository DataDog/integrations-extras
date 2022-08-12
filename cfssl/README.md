# Agent Check: cfssl

## Overview

This check monitors [cfssl][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][4] for guidance on applying these instructions.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the cfssl check on your host. See [Use Community Integrations][2] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-cfssl==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][8].

### Configuration

1. Edit the `cfssl.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your cfssl performance data. See the [sample exim.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `cfssl` under the Checks section.

## Data Collected

### Metrics

The cfssl integration does not include any metrics.

### Events

The cfssl integration does not include any events.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][10].


[1]: https://github.com/cloudflare/cfssl
[2]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/cfssl/datadog_checks/cfssl/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://docs.datadoghq.com/getting_started/integrations/
[9]: https://github.com/DataDog/integrations-extras/blob/master/cfssl/assets/service_checks.json
[10]: https://www.datadoghq.com/support/
