# Reboot Required

## Overview

Linux systems that are configured to autoinstall packages may not be configured to autoreboot (it may be desirable to time this manually). This check enables alerts to be fired in the case where reboots are not performed in a timely manner.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Reboot Required check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent prior to version 6.8][2] or the [Docker Agent][3]:

1. [Download and launch the Datadog Agent][4].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-reboot_required==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][5].

### Configuration

1. Edit the `reboot_required.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6]. See the [sample reboot_required.d/conf.yaml][7] for all available configuration options.

2. Make sure you create a dd-agent (user that runs the Datadog agent) writable directory for the agent, and used by this check. The default of `/var/run/dd-agent` is ideal. The snippet below should suffice.

   ```shell
   sudo mkdir /var/run/dd-agent
   sudo chown dd-agent:dd-agent /var/run/dd-agent
   ```

3. [Restart the Agent][8].

### Validation

[Run the Agent's `status` subcommand][9] and look for `reboot_required` under the Checks section.

## Data Collected

### Metrics

No metrics are collected.

### Events

The reboot_required check does not include any events.

## Service Checks

To create alert conditions on these service checks in Datadog, select 'Custom Check' on the [Create Monitor][10] page, not 'Integration'.

**`system.reboot_required`**

The check returns:

- `OK` if the system does not require a reboot or for less than `days_warning` or `days_critical`.
- `WARNING` if the system has required a reboot for longer than `days_warning` days.
- `CRITICAL` if the system has required a reboot for longer than `days_critical` days.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/reboot_required/datadog_checks/reboot_required/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://app.datadoghq.com/monitors#/create
[11]: http://docs.datadoghq.com/help
