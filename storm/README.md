# Storm Integration

## Overview

Get metrics from Storm service in real time to:

- Visualize and monitor Storm cluster and topology metrics.
- Be notified about Storm failovers and events.

## Setup

The Storm check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Storm check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `storm` package, run:

   ```shell
   ddev -e release build storm
   ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_STORM_ARTIFACT_>/<STORM_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `storm.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Storm [metrics](#metrics). See the [sample storm.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

## Validation

[Run the Agent's `status` subcommand][11] and look for `storm` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this check.

### Events

The Storm check does not include any events.

### Service Checks

**`topology_check.{TOPOLOGY NAME}`**

The check returns:

- `OK` if the topology is active.
- `CRITICAL` if the topology is not active.

## Troubleshooting

Need help? Contact [Datadog support][13].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/storm/datadog_checks/storm/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[12]: https://github.com/DataDog/integrations-extras/blob/master/storm/metadata.csv
[13]: http://docs.datadoghq.com/help
