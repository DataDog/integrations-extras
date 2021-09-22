# Sortdb Integration

## Overview

Get metrics from [Sortdb][1] service in real time to:

- Visualize and monitor Sortdb stats.
- Be notified about Sortdb failovers.
- Check health of and get stats from multiple instances

## Setup

The Sortdb check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Sortdb check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-sortdb==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `sortdb.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Sortdb [metrics](#metric-collection). See the [sample sortdb.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `sortdb` under the Checks section.

## Compatibility

The SortDB check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

The SortDB check does not currently include any events.


[1]: https://github.com/jehiah/sortdb
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/datadog_checks/sortdb/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/metadata.csv
[12]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/assets/service_checks.json
