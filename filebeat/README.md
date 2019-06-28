# Filebeat Integration

## Overview

Get metrics from Filebeat service in real time to:

* Visualize and monitor Filebeat states.
* Be notified about Filebeat failovers and events.

## Setup

The Filebeat check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Filebeat check on your host. See our dedicated Agent guide about [how to install Community integrations][2] to discover how to install them with the [Agent prior to version 6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `filebeat` package, run:

    ```
    ddev -e release build filebeat
    ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_FILEBEAT_ARTIFACT_>/<FILEBEAT_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `filebeat.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Filebeat [metrics](#metric-collection).
  See the [sample filebeat.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

## Validation

[Run the Agent's `status` subcommand][11] and look for `filebeat` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][12] for a list of metrics provided by this check.

### Events
The Filebeat check does not include any events.

### Service Checks
The Filebeat check does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][13].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/filebeat/datadog_checks/filebeat/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[12]: https://github.com/DataDog/integrations-extras/blob/master/filebeat/metadata.csv
[13]: https://docs.datadoghq.com/help
