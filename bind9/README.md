# Bind9 check Integration

## Overview

Get metrics from Bind9 DNS Server.

- Visualize and monitor bind9 stats

![Snap][1]

## Setup

The Bind9 check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Bind9 check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-bind9==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `bind9.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Bind9 [metrics](#metrics). See the [sample bind9.d/conf.yaml][8] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - url: "<BIND_9_STATS_URL>"
   ```

2. [Restart the Agent][9]

### Validation

[Run the Agent's `status` subcommand][10] and look for `bind9` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Events

The bind9_check check does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][13].


[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bind9/images/snapshot.png
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/bind9/datadog_checks/bind9/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/bind9/metadata.csv
[12]: https://github.com/DataDog/integrations-extras/blob/master/bind9/assets/service_checks.json
[13]: https://docs.datadoghq.com/help
