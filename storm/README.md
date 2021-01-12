# Storm Integration

## Overview

Get metrics from Storm service in real time to:

- Visualize and monitor Storm cluster and topology metrics.
- Be notified about Storm failovers and events.

## Setup

The Storm check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Aqua check on your host. See our dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior to version 6.8][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][1].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `storm.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your Storm [metrics](#metrics). See the [sample storm.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8]

## Validation

[Run the Agent's `status` subcommand][9] and look for `storm` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Events

The Storm check does not include any events.

### Service Checks

**`topology_check.{TOPOLOGY NAME}`**

The check returns:

- `OK` if the topology is active.
- `CRITICAL` if the topology is not active.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/storm/datadog_checks/storm/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/storm/metadata.csv
[11]: http://docs.datadoghq.com/help
