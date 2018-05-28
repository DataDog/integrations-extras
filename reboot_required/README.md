# Reboot Required

## Overview

Linux systems that are configured to autoinstall packages may not be configured to autoreboot (it may be desirable to time this manually). This check will enable alerts to be fired in the case where reboots are not performed in a timely manner.

## Setup
The Reboot Required check is **NOT** included in the [Datadog Agent][1] package.
### Installation

To install the Reboot Required check on your host:

1. [Download the Datadog Agent][1]
2. Download the [`check.py` file][7] for Reboot Required
3. Place it in the Agent's `checks.d` directory, 
4. Rename it to `reboot_required.py`.

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

No metrics are collected at this time.

### Events

The reboot_required check does not include any events at this time.

## Service Checks

To create alert conditions on these service checks in Datadog, select 'Custom Check' on the [Create Monitor][4] page, not 'Integration'.

**`system.reboot_required`**

The check returns:
* `OK` if the system does not require a reboot or for less than `days_warning` or `days_critical`.
* `WARNING` if the system has required a reboot for longer than `days_warning` days.
* `CRITICAL` if the system has required a reboot for longer than `days_critical` days.

## Troubleshooting
Need help? Contact [Datadog Support][5].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/reboot_required/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[4]: https://app.datadoghq.com/monitors#/create
[5]: http://docs.datadoghq.com/help/
[6]: https://www.datadoghq.com/blog/
[7]: https://github.com/DataDog/integrations-extras/blob/master/reboot_required/check.py
