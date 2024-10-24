# Agent Check: Kepler

## Overview

This check monitors [Kepler][1].

## Setup

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Kepler check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the integration:

   ```shell
   datadog-agent integration install -t datadog-kepler==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration


1. Edit the `kepler.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your kepler performance data. See the [sample kepler.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `kepler` under the Checks section.

## Data Collected

### Metrics

Kepler does not include any metrics.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration.

### Events

Kepler does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://sustainable-computing.io/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/kepler/datadog_checks/kepler/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/kepler/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/kepler/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/

