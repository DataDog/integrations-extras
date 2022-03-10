# Reboot Required

## Overview

Linux systems that are configured to autoinstall packages may not be configured to autoreboot (it may be desirable to time this manually). This check enables alerts to be fired in the case where reboots are not performed in a timely manner.

## Setup

The Reboot Required check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Reboot Required check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-reboot_required==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

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

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][11].


[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/reboot_required/datadog_checks/reboot_required/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://app.datadoghq.com/monitors#/create
[11]: http://docs.datadoghq.com/help
[12]: https://github.com/DataDog/integrations-extras/blob/master/reboot_required/assets/service_checks.json
