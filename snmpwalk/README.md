# Snmpwalk Integration

## Overview

Get metrics from SNMP walk service in real time to:

* Visualize and monitor SNMP walk states
* Be notified about SNMP walk failovers and events.


## Setup

The SNMP walk check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the SNMP walk check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][1].
2. Download the [`snmpwalk.py` file][7] for SNMP walk.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:

1. Install the [developer toolkit][3] on any machine.
2. Run `ddev release build snmpwalk` to build the package.
3. [Download the Datadog Agent][1].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/snmpwalk/dist/<ARTIFACT_NAME>.whl`.

### Configuration

To configure the SNMP walk check:

1. Create a `snmpwalk.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `snmpwalk.d/` folder previously created.
3. Consult the [sample snmpwalk.yaml][6] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `snmpwalk` under the Checks section.

## Data Collected
### Metrics
The SNMP walk check does not include any metrics.

### Events
The SNMP walk check does not include any events.

### Service Checks
**`snmpwalk.can_check`**

The check returns:

* `OK` if the check can collect metrics from `snmpwalk`.
* `CRITICAL` if check encounters an error when trying to collect metrics from `snmpwalk`.

## Troubleshooting
Need help? Contact [Datadog support][5].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: http://docs.datadoghq.com/help/
[6]: https://github.com/DataDog/integrations-extras/blob/master/snmpwalk/datadog_checks/snmpwalk/data/conf.yaml.example
[7]: https://github.com/DataDog/integrations-extras/blob/master/snmpwalk/datadog_checks/snmpwalk/snmpwalk.py

