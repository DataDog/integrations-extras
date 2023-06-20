# Gnatsd_streaming Integration

## Overview

Get metrics from gnatsd_streaming service in real time to:

- Visualize and monitor gnatsd_streaming states
- Be notified about gnatsd_streaming failovers and events.

## Setup

The gnatsd_streaming check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the gnatsd_streaming check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-gnatsd_streaming==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `gnatsd_streaming.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your GnatsD streaming [metrics](#metrics).
   See the [sample gnatsd_streaming.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8]

### Validation

[Run the Agent's status subcommand][9] and look for `gnatsd_streaming` under the Checks section.

## Compatibility

The gnatsd_streaming check is compatible with all major platforms

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

Nats Streaming Server metrics are tagged with names like "nss-cluster_id"

### Events

If you are running Nats Streaming Server in a Fault Tolerant group, a Nats Streaming Failover event is issued when the status of a server changes between `FT_STANDBY` and `FT_ACTIVE`.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][11].


[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd_streaming/datadog_checks/gnatsd_streaming/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv
[11]: http://docs.datadoghq.com/help
[12]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd_streaming/assets/service_checks.json
