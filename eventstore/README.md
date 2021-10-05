# EventStore Integration

## Overview

Get metrics from EventStore in real time to:

* Visualize and monitor EventStore queues
* Capture all available metrics within the following API endpoints: stats, node info, non-transient projections, subscriptions, cluster gossip (the list of endpoints to scrape is configurable)

## Setup

The EventStore check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the EventStore check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-eventstore==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `eventstore.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your EventStore [metrics](#metrics).
   See the [sample eventstore.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `eventstore` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Events

The eventstore check does not include any events.

### Service Checks

The eventstore check does not include any service checks.

## Troubleshooting

Need help? Contact the [maintainer][11] of this integration.

[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/datadog_checks/eventstore/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/manifest.json
