# Filebeat Integration

## Overview

Get metrics from Filebeat service in real time to:

- Visualize and monitor Filebeat states.
- Be notified about Filebeat failovers and events.

## Setup

The Filebeat check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Filebeat check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-filebeat==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `filebeat.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Filebeat [metrics](#metrics). See the [sample filebeat.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

## Validation

Run the [Agent's status subcommand][10] and look for `filebeat` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Events

The Filebeat check does not include any events.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].


[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/filebeat/datadog_checks/filebeat/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/filebeat/metadata.csv
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/filebeat/assets/service_checks.json
