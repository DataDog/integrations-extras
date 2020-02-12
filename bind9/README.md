# Bind9 check Integration

## Overview

Get metrics from Bind9 DNS Server.

- Visualize and monitor bind9 stats

![Snap][1]

## Setup

The Bind9 check is **NOT** included in the [Datadog Agent][2] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Bind9 check on your host. See our dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior v6.8][4] or the [Docker Agent][5]:

1. Install the [developer toolkit][6].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `bind9` package, run:

   ```shell
   ddev -e release build bind9
   ```

5. [Download and launch the Datadog Agent][2].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_BIND9_ARTIFACT>/<BIND9_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `bind9.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Bind9 [metrics](#metrics). See the [sample bind9.d/conf.yaml][9] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - URL: "<BIND_9_STATS_URL>"
   ```

2. [Restart the Agent][10]

### Validation

[Run the Agent's `status` subcommand][11] and look for `bind9` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this integration.

### Events

The bind9_check check does not include any event at this time.

### Service Checks

`bind9_check.BIND_SERVICE_CHECK` : Returns `OK` If Statistics-channel URL of DNS is present in Instance.
`bind9_check.BIND_SERVICE_CHECK` : Returns `CRITICAL` If URL Errors occurs.

## Development

Please refer to the [main documentation][13] for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bind9/images/snapshot.png
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/bind9/datadog_checks/bind9/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[12]: https://github.com/DataDog/cookiecutter-datadog-check/blob/master/%7B%7Bcookiecutter.check_name%7D%7D/metadata.csv
[13]: https://docs.datadoghq.com/developers
