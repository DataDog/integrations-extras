# Snmpwalk Integration

## Overview

Get metrics from SNMP walk service in real time to:

* Visualize and monitor SNMP walk states
* Be notified about SNMP walk failovers and events.


## Setup

The SNMP walk check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the SNMP walk check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `snmpwalk` package, run:

    ```
    ddev -e release build snmpwalk
    ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_SNMPWALK_ARTIFACT_>/<SNMPWALK_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `snmpwalk.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your SNMP walk [metrics](#metrics).
  See the [sample snmpwalk.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

## Validation

[Run the Agent's `status` subcommand][11] and look for `snmpwalk` under the Checks section.

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
Need help? Contact [Datadog support][12].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/snmpwalk/datadog_checks/snmpwalk/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[12]: http://docs.datadoghq.com/help
