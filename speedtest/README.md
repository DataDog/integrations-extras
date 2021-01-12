# Agent Check: Speedtest

## Overview

This check monitors [Speedtest][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Aqua check on your host. See the dedicated Agent guide for [installing community integrations][4] to install checks with the [Agent prior to version 6.8][5] or the [Docker Agent][6]:

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```
3. Configure your integration like [any other packaged integration][7].

Note: For all hosts you need to also install [Speedtest CLI][1] on your host and accept the agreement as the Datadog Agent user (e.g. `sudo -u dd-agent speedtest`) prior to use.

### Configuration

1. Edit the `speedtest.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Speedtest performance data. See the [sample speedtest.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `speedtest` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Service Checks

Speedtest does not include any service checks.

### Events

Speedtest does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://www.speedtest.net/apps/cli
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[6]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[7]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://github.com/DataDog/integrations-extras/blob/master/speedtest/datadog_checks/speedtest/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[11]: https://github.com/DataDog/integrations-extras/blob/master/speedtest/metadata.csv
[12]: https://docs.datadoghq.com/help/
