# Gnatsd_streaming Integration

## Overview

Get metrics from gnatsd_streaming service in real time to:

- Visualize and monitor gnatsd_streaming states
- Be notified about gnatsd_streaming failovers and events.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the gnatsd_streaming check on your host. See our dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent prior v6.8][2] or the [Docker Agent][3]:

1. Install the [developer toolkit][4].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `gnatsd_streaming` package, run:

   ```shell
   ddev -e release build gnatsd_streaming
   ```

5. [Download and launch the Datadog Agent][5].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_GNATSD_STREAMING_ARTIFACT_>/<GNATSD_STREAMING_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `gnatsd_streaming.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your GnatsD streaming [metrics](#metric-collection).
   See the [sample gnatsd_streaming.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

### Validation

[Run the Agent's status subcommand][10] and look for `gnatsd_streaming` under the Checks section.

## Compatibility

The gnatsd_streaming check is compatible with all major platforms

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

Nats Streaming Server metrics are tagged with names like "nss-cluster_id"

### Events

If you are running Nats Streaming Server in a Fault Tolerant group a Nats Streaming Failover event will be issued
when the status of a Server changes between `FT_STANDBY` and `FT_ACTIVE`

### Service Checks

This gnatsd_streaming check tags all service checks it collects with:

- `server_name:<server_name_in_yaml>`
- `url:<host_in_yaml>`

`gnatsd_streaming.can_connect`:
Returns `CRITICAL` if the Agent fails to receive a 200 from the _monitoring_ endpoint, otherwise returns `OK`.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd_streaming/datadog_checks/gnatsd_streaming/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv
[12]: http://docs.datadoghq.com/help
