# Agent Check: Puma

## Overview

This check monitors [Puma][1] through the Datadog Agent via the Puma metrics endpoint provided by the [control/status][2] server.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Puma check on your host. See the dedicated Agent guide for [installing community integrations][4] to install checks with the [Agent prior to version 6.8][5] or the [Docker Agent][6]:

1. [Download the Datadog Agent][7].

2. Run the following command to install the integrations wheel with the Agent:

   ```shell
      datadog-agent integration install -t datadog-puma==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][8].


### Configuration

1. Edit the `puma.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Puma performance data. See the [sample puma.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10].

### Validation

[Run the Agent's status subcommand][11] and look for `puma` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this check.

### Service Checks

**puma.connection**: Returns `CRITICAL` if the Agent is unable to connect to the monitored Puma instance. Returns `OK` otherwise.

### Events

Puma does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][13].

[1]: https://puma.io/
[2]: https://github.com/puma/puma#controlstatus-server
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[6]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[7]: https://app.datadoghq.com/account/settings#agent
[8]: https://docs.datadoghq.com/getting_started/integrations/
[9]: https://github.com/DataDog/integrations-extras/blob/master/puma/datadog_checks/puma/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[12]: https://github.com/DataDog/integrations-extras/blob/master/puma/metadata.csv
[13]: https://docs.datadoghq.com/help/
