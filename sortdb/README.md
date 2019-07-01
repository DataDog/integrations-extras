# Sortdb Integration

## Overview

Get metrics from [Sortdb][1] service in real time to:

* Visualize and monitor Sortdb stats.
* Be notified about Sortdb failovers.
* Check health of and get stats from multiple instances

## Installation

If you are using Agent v6.8+ follow the instructions below to install the Sortdb check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `sortdb` package, run:

    ```
    ddev -e release build sortdb
    ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_SORTDB_ARTIFACT_>/<SORTDB_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][7].

## Configuration

1. Edit the `sortdb.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Sortdb [metrics](#metric-collection).
  See the [sample sortdb.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

## Validation

[Run the Agent's status subcommand][11] and look for `sortdb` under the Checks section.

## Compatibility

The SortDB check check is compatible with all major platforms

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this integration.

### Service Checks

The SortDB check does not currently include any service checks.

### Events

The SortDB check does not currently include any events.

[1]: https://github.com/jehiah/sortdb
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/datadog_checks/sortdb/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[12]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/metadata.csv
