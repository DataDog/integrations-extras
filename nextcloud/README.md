# Agent Check: Nextcloud

## Overview

This check monitors [Nextcloud][1].

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Nextcloud check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]: your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `nextcloud` package, run:

   ```shell
   ddev -e release build nextcloud
   ```

1. [Download and launch the Datadog Agent][5].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `nextcloud.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Nextcloud [metrics](#metrics). See the [sample nextcloud.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

### Validation

[Run the Agent's `status` subcommand][10] and look for `nextcloud` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Service Checks

**`nextcloud.can_connect`**

The check returns:

- `OK` if Nextcloud is reachable.
- `CRITICAL` if Nextcloud is unreachable.

### Events

Nextcloud does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://nextcloud.com
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/nextcloud/datadog_checks/nextcloud/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/nextcloud/metadata.csv
[12]: https://docs.datadoghq.com/help/
