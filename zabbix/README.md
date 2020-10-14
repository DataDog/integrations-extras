# Agent Check: Zabbix

## Overview

This check monitors [Zabbix][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host.

### Installation

To install the Zabbix check on your host:

1. Install the [developer toolkit][2] on any machine.
2. Run `ddev release build zabbix` to build the package.
3. [Download the Datadog Agent][3].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/zabbix/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `zabbix.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Zabbix performance data. See the [sample zabbix.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `zabbix` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Service Checks

Zabbix does not include any service checks.

### Events

Zabbix does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][8].

[1]: https://www.zabbix.com/
[2]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://github.com/DataDog/integrations-extras/blob/master/zabbix/datadog_checks/zabbix/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/zabbix/metadata.csv
[8]: https://docs.datadoghq.com/help/
