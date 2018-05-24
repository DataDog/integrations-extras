# Snmpwalk Integration

## Overview

Get metrics from SNMP walk service in real time to:

* Visualize and monitor SNMP walk states
* Be notified about SNMP walk failovers and events.

## Setup

### Configuration

Edit the `snmpwalk.yaml` file to point to your server and port, set the masters to monitor.

### Validation

[Run the Agent's `status` subcommand][1] and look for `snmpwalk` under the Checks section.

## Data Collected
### Metrics

The SNMP walk check does not include any metrics at this time.

### Events
The SNMP walk check does not include any events at this time.

### Service Checks
The SNMP walk check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][2].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][3].

[1]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[2]: http://docs.datadoghq.com/help/
[3]: https://www.datadoghq.com/blog/
