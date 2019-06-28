# Gnatsd Integration

## Overview

Get metrics from Gnatsd service in real time to:

* Visualize and monitor Gnatsd states
* Be notified about Gnatsd failovers and events.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Gnatsd check on your host. See our dedicated Agent guide about [how to install Community integration][1] to see how to install them with the [Agent prior v6.8][2] or the [Docker Agent][3]:

1. Install the [developer toolkit][4].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `gnatsd` package, run:

    ```
    ddev -e release build gnatsd
    ```

5. [Download and launch the Datadog Agent][5].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_GNATSD_ARTIFACT_>/<GNATSD_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][6].
8. [Restart the Agent][7].

### Configuration

1. Edit the `gnatsd.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Gnatsd [metrics](#metrics).
  See the [sample gnatsd.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

### Validation

[Run the Agent's status subcommand][11] and look for `gnatsd` under the Checks section.

## Compatibility

The gnatsd check is compatible with all major platforms

## Data Collected
### Metrics

See [metadata.csv][12] for a list of metrics provided by this integration.

**Note**: If you use custom Nats cluster names, your metrics may look like this:
`gnatsd.connz.connections.cluster_name.in_msgs`

### Events
The gnatsd check does not include any events.

### Service Checks
This gnatsd check tags all service checks it collects with:

* `server_name:<server_name_in_yaml>`
* `url:<host_in_yaml>`

`gnatsd.can_connect`:
Returns `CRITICAL` if the Agent fails to receive a 200 from the _monitoring_ endpoint, otherwise returns `OK`.

## Troubleshooting
Need help? Contact [Datadog support][13].

[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#restart-the-agent
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd/datadog_checks/gnatsd/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[12]: https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv
[13]: https://docs.datadoghq.com/help
