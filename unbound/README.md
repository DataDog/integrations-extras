# Agent Check: Unbound

## Overview

This check monitors [Unbound][1] through the Datadog Agent.

Get metrics from unbound service in real time to:

- Visualize and monitor unbound states

## Setup

The Unbound check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Unbound check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-unbound==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `unbound.d/conf.yaml` file, in the `conf.d/` folder at the root of
   your Agent's configuration directory to start collecting unbound metrics. See
   the [sample unbound.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `unbound` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Events

The Unbound check does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][11].


[1]: https://nlnetlabs.nl/documentation/unbound/unbound-control/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/unbound/datadog_checks/unbound/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/unbound/metadata.csv
[11]: https://docs.datadoghq.com/help/
[12]: https://github.com/DataDog/integrations-extras/blob/master/unbound/assets/service_checks.json
