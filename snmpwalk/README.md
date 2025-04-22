# Snmpwalk Integration

## Overview

Get metrics from SNMP walk service in real time to:

- Visualize and monitor SNMP walk states
- Be notified about SNMP walk failovers and events.

## Setup

The SNMP walk check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the SNMP walk check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-snmpwalk==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `snmpwalk.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your SNMP walk [metrics](#metrics). See the [sample snmpwalk.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

## Validation

[Run the Agent's `status` subcommand][9] and look for `snmpwalk` under the Checks section.

## Data Collected

### Metrics

The SNMP walk check does not include any metrics.

### Events

The SNMP walk check does not include any events.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][10].


[2]: /account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/snmpwalk/datadog_checks/snmpwalk/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: http://docs.datadoghq.com/help
[11]: https://github.com/DataDog/integrations-extras/blob/master/snmpwalk/assets/service_checks.json
