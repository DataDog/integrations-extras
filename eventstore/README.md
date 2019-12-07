# EventStore Integration

## Overview

Get metrics from EventStore in real time to:

* Visualize and monitor EventStore queues
* Capture all available metrics within the following API endpoints: stats, node info, non-transient projections, subscriptions, cluster gossip (the list of endpoints to scrape is configurable)

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the EventStore check on your host. See our dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent prior to version 6.8][2] or the [Docker Agent][3]:

1. Install the [developer toolkit][4].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `eventstore` package, run:

   ```shell
   ddev -e release build eventstore
   ```

5. [Download and launch the Datadog Agent][5].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_EVENTSTORE_ARTIFACT_>/<EVENTSTORE_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `eventstore.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your EventStore [metrics](#metrics).
   See the [sample eventstore.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `eventstore` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Events

The eventstore check does not include any events.

### Service Checks

The eventstore check does not include any service checks.

## Troubleshooting

Need help? Contact the [maintainer][12] of this integration.

[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/datadog_checks/eventstore/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/metadata.csv
[12]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/manifest.json
