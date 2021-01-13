# Snmpwalk Integration

## Overview

Get metrics from SNMP walk service in real time to:

- Visualize and monitor SNMP walk states
- Be notified about SNMP walk failovers and events.

## Setup

The SNMP walk check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the SNMP walk check on your host. See the dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. [Download and launch the Datadog Agent][1].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][5].

### Configuration

1. Edit the `snmpwalk.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your SNMP walk [metrics](#metrics). See the [sample snmpwalk.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8]

## Validation

[Run the Agent's `status` subcommand][9] and look for `snmpwalk` under the Checks section.

## Data Collected

### Metrics

The SNMP walk check does not include any metrics.

### Events

The SNMP walk check does not include any events.

### Service Checks

**`snmpwalk.can_check`**

The check returns:

- `OK` if the check can collect metrics from `snmpwalk`.
- `CRITICAL` if check encounters an error when trying to collect metrics from `snmpwalk`.

## Troubleshooting

Need help? Contact [Datadog support][10].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/snmpwalk/datadog_checks/snmpwalk/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: http://docs.datadoghq.com/help
