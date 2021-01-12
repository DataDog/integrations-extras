# Sortdb Integration

## Overview

Get metrics from [Sortdb][1] service in real time to:

- Visualize and monitor Sortdb stats.
- Be notified about Sortdb failovers.
- Check health of and get stats from multiple instances

## Setup 

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Sortdb check on your host. See the dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]: your `ddev` config with the `integrations-extras/` path:

1. [Download and launch the Datadog Agent][5].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `sortdb.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Sortdb [metrics](#metric-collection). See the [sample sortdb.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

### Validation

[Run the Agent's status subcommand][10] and look for `sortdb` under the Checks section.

## Compatibility

The SortDB check check is compatible with all major platforms

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Service Checks

The SortDB check does not currently include any service checks.

### Events

The SortDB check does not currently include any events.

[1]: https://github.com/jehiah/sortdb
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/datadog_checks/sortdb/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/metadata.csv
