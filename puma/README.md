# Agent Check: Puma

## Overview

This check monitors [Puma][1] through the Datadog Agent via the Puma metrics endpoint provided by the [control/status][2] server.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

To install the Puma check on your host:

2. Run `ddev release build puma` to build the package.
3. [Download the Datadog Agent][4].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>`.

### Configuration

1. Edit the `puma.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Puma performance data. See the [sample puma.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `puma` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

**puma.connection**: Returns `CRITICAL` if the Agent is unable to connect to the monitored Puma instance. Returns `OK` otherwise.

### Events

Puma does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://puma.io/
[2]: https://github.com/puma/puma#controlstatus-server
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://github.com/DataDog/integrations-extras/blob/master/puma/datadog_checks/puma/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/puma/metadata.csv
[9]: https://docs.datadoghq.com/help/
