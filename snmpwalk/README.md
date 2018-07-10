# Snmpwalk Integration

## Overview

Get metrics from SNMP walk service in real time to:

* Visualize and monitor SNMP walk states
* Be notified about SNMP walk failovers and events.


## Setup

The SNMP walk check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the SNMP walk check on your host:

1. [Download the Datadog Agent][1].
2. Download the [`check.py` file][2] for SNMP walk.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `snmpwalk.py`.

### Configuration

To configure the SNMP walk check:

1. Create a `snmpwalk.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `snmpwalk.d/` folder previously created.
3. Consult the [sample snmpwalk.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `snmpwalk` under the Checks section.

## Data Collected
### Metrics
The SNMP walk check does not include any metrics at this time.

### Events
The SNMP walk check does not include any events at this time.

### Service Checks
**`snmpwalk.can_check`**

The check returns:

* `OK` if the check can collect metrics from `snmpwalk`.
* `CRITICAL` if check encounters an error when trying to collect metrics from `snmpwalk`.

## Troubleshooting
Need help? Contact [Datadog Support][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/metadata.csv
[6]: http://docs.datadoghq.com/help/
