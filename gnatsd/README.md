# Gnatsd Integration

## Overview

Get metrics from Gnatsd service in real time to:

- Visualize and monitor Gnatsd states
- Be notified about Gnatsd failovers and events.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Gnatsd check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent prior to version 6.8][2] or the [Docker Agent][3]:

1. [Download and launch the Datadog Agent][4].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-gnatsd==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][5].

### Configuration

1. Edit the `gnatsd.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your Gnatsd [metrics](#metrics). See the [sample gnatsd.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8]

### Validation

[Run the Agent's status subcommand][9] and look for `gnatsd` under the Checks section.

## Compatibility

The gnatsd check is compatible with all major platforms

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

**Note**: If you use custom Nats cluster names, your metrics may look like this:
`gnatsd.connz.connections.cluster_name.in_msgs`

### Events

The gnatsd check does not include any events.

### Service Checks

This gnatsd check tags all service checks it collects with:

- `server_name:<server_name_in_yaml>`
- `url:<host_in_yaml>`

`gnatsd.can_connect`:
Returns `CRITICAL` if the Agent fails to receive a 200 from the _monitoring_ endpoint, otherwise returns `OK`.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd/datadog_checks/gnatsd/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv
[11]: https://docs.datadoghq.com/help/
