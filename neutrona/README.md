# Agent Check: Neutrona

## Overview

This check monitors [Neutrona][1] cloud connectivity services to:

- Azure (ExpressRoute)

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Neutrona check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `neutrona` package, run:

   ```shell
   ddev -e release build neutrona
   ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_NEUTRONA_ARTIFACT_>/<NEUTRONA_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `neutrona.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Neutrona [metrics](#metric-collection).
   See the [sample neutrona.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

### Validation

[Run the Agent's status subcommand][11] and look for `neutrona` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this integration.

### Service Checks

Neutrona does not include any service checks at this time.

### Events

Neutrona does not include any events at this time.

## Troubleshooting

Need help? Contact [Datadog support][13].

[1]: https://telemetry.neutrona.com
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/neutrona/datadog_checks/neutrona/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[12]: https://github.com/DataDog/integrations-core/blob/master/neutrona/metadata.csv
[13]: https://docs.datadoghq.com/help
