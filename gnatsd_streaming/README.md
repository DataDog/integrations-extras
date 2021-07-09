# Gnatsd_streaming Integration

## Overview

Get metrics from gnatsd_streaming service in real time to:

- Visualize and monitor gnatsd_streaming states
- Be notified about gnatsd_streaming failovers and events.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the gnatsd_streaming check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent prior v6.8][2] or the [Docker Agent][3]:

1. [Download and launch the Datadog Agent][4].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-gnatsd_streaming==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][5].

### Configuration

1. Edit the `gnatsd_streaming.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your GnatsD streaming [metrics](#metric-collection).
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

If you are running Nats Streaming Server in a Fault Tolerant group a Nats Streaming Failover event will be issued
when the status of a Server changes between `FT_STANDBY` and `FT_ACTIVE`

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][11].


[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd_streaming/datadog_checks/gnatsd_streaming/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv
[11]: http://docs.datadoghq.com/help
[12]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd_streaming/assets/service_checks.json
