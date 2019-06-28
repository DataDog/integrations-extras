
# Bind9 check Integration

## Overview

Get metrics from Bind9 DNS Server.

* Visualize and monitor bind9 stats
![Snap][1]

## Setup

The Bind9 check is **NOT** included in the [Datadog Agent][2] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Bind9 check on your host. See our dedicated Agent guide about [how to install Community integration][3] to see how to install them with the [Agent prior v6.8][4] or the [Docker Agent][5]:

1. Install the [developer toolkit][6].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `bind9` package, run:

    ```
    ddev -e release build bind9
    ```

5. [Download and launch the Datadog Agent][2].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_BIND9_ARTIFACT>/<BIND9_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][7].
8. [Restart the Agent][8].

### Configuration

1. Edit the `bind9.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][9] to start collecting your Bind9 [metrics](#metric-collection).
  See the [sample bind9.d/conf.yaml][10] for all available configuration options.

2. [Restart the Agent][11]

#### Metric Collection

Add this configuration setup to your `conf.yaml` file to start gathering your [metrics][12]:

```
init_config:

instances:
  - URL : <BIND_9_STATS_URL>
```

### Validation

[Run the Agent's `status` subcommand][13] and look for `bind9` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][14] for a list of metrics provided by this integration.

### Events

The bind9_check check does not include any event at this time.

### Service Checks

`bind9_check.BIND_SERVICE_CHECK` : Returns `OK` If Statistics-channel URL of DNS is present in Instance.
`bind9_check.BIND_SERVICE_CHECK` : Returns `CRITICAL` If URL Errors occurs.

## Development

Please refer to the [main documentation][15] for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bind9/images/snapshot.png
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[10]: https://github.com/DataDog/integrations-extras/blob/master/bind9/datadog_checks/bind9/data/conf.yaml.example
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[12]: #metrics
[13]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[14]: https://github.com/DataDog/cookiecutter-datadog-check/blob/master/%7B%7Bcookiecutter.check_name%7D%7D/metadata.csv
[15]: https://docs.datadoghq.com/developers
