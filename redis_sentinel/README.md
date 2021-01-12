# Redis Sentinel

## Overview

Get metrics from Redis's Sentinel service in real time to:

- Visualize and monitor sentinels states
- Be notified about failovers

## Setup

The Redis's Sentinel check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Redis's Sentinel check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. [Download and launch the Datadog Agent][6].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_REDIS_SENTINEL_ARTIFACT_>/<REDIS_SENTINEL_ARTIFACT_NAME>.whl
   ```

3. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `redis_sentinel.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Redis Sentinel [metrics](#metrics).
   See the [sample upsc.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

## Validation

[Run the Agent's `status` subcommand][11] and look for `redis_sentinel` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this check.

### Events

The Redis's Sentinel check does not include any events.

### Service Checks

**`redis.sentinel.master_is_down`**

The check returns:

- `OK` if the master is up.
- `CRITICAL` if the master is down.

**`redis.sentinel.master_is_disconnected`**

The check returns:

- `OK` if the master is not disconnected.
- `CRITICAL` if the master is disconnected.

**`redis.sentinel.slave_master_link_down`**

The check returns:

- `OK` if the master link status is ok.
- `CRITICAL` if the master link status is not ok.

**`redis.sentinel.slave_is_disconnected`**

The check returns:

- `OK` if the slave is not disconnected.
- `CRITICAL` if the slave is disconnected.

## Troubleshooting

Need help? Contact [Datadog support][13].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/datadog_checks/redis_sentinel/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[12]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/metadata.csv
[13]: http://docs.datadoghq.com/help
