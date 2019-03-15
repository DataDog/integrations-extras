# Reboot Required

## Overview

Linux systems that are configured to autoinstall packages may not be configured to autoreboot (it may be desirable to time this manually). This check will enable alerts to be fired in the case where reboots are not performed in a timely manner.

## Setup

### Installation

To install the Reboot Required check on your host:

1. Install the [developer toolkit][6] on any machine.
2. Run `ddev release build reboot_required` to build the package.
3. [Download the Datadog Agent][1].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/reboot_required/dist/<ARTIFACT_NAME>.whl`.

### Configuration

To configure the Reboot Required check:

1. Create a `reboot_required.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `reboot_required.d/` folder previously created.
3. Consult the [sample reboot_required.yaml][2] file and copy its content in the `conf.yaml` file. Minimum configuration should include:

    ```
    init_config:
    instances:
        - reboot_signal_file: "/var/run/reboot-required"
    ```

4. Make sure you create a dd-agent (user that runs the Datadog agent) writable directory for the agent, and used by this check. The default of /var/run/dd-agent is ideal. The snippet below should suffice.

    ```
    sudo mkdir /var/run/dd-agent
    sudo chown dd-agent:dd-agent /var/run/dd-agent
    ```

5. [Restart the Agent][3].

### Validation

[Run the Agent's `status` subcommand][3] and look for `reboot_required` under the Checks section.

## Data Collected

### Metrics

No metrics are collected.

### Events

The reboot_required check does not include any events.

## Service Checks

To create alert conditions on these service checks in Datadog, select 'Custom Check' on the [Create Monitor][4] page, not 'Integration'.

**`system.reboot_required`**

The check returns:

* `OK` if the system does not require a reboot or for less than `days_warning` or `days_critical`.
* `WARNING` if the system has required a reboot for longer than `days_warning` days.
* `CRITICAL` if the system has required a reboot for longer than `days_critical` days.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/reboot_required/datadog_checks/reboot_required/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[4]: https://app.datadoghq.com/monitors#/create
[5]: http://docs.datadoghq.com/help/
[6]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
