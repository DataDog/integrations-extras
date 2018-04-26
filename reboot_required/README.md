# Reboot Required

## Overview

Linux systems that are configured to autoinstall packages may not be configured to autoreboot (it may be desirable to time this manually). This check will enable alerts to be fired in the case where reboots are not performed in a timely manner.

## Setup
### Installation

The directory check is packaged with the Agent, so simply [install the Agent][1] anywhere you wish to use it.

Make sure you create a dd-agent (user that runs the Datadog agent) writeable directory for the agent, and used by this check. The default of /var/run/dd-agent is ideal. The snippet below should suffice.

```
sudo mkdir /var/run/dd-agent
sudo chown dd-agent:dd-agent /var/run/dd-agent 
```

### Configuration

1. Edit your `reboot_required.yaml` file in the Agent's `conf.d` directory. See the [sample reboot_required.yaml][2] for all available configuration options:

### Validation

[Run the Agent's `info` subcommand][3] and look for `reboot_required` under the Checks section:

```
  Checks
  ======
    [...]

    reboot_required 
    -------
      - instance #0 [OK]
      - Collected 0 metrics, 0 events & 1 service check

    [...]
```

## Compatibility

The reboot_required check is currently only compatible with Linux systems.

## Data Collected

### Metrics

No metrics are collected at this time.

### Events

The reboot_required check does not include any events at this time.

## Service Checks

To create alert conditions on these service checks in Datadog, select 'Custom Check' on the [Create Monitor][4] page, not 'Integration'.

**`system.reboot_required`**:

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
[3]: https://docs.datadoghq.com/agent/faq/agent-status-and-information/
[4]: https://app.datadoghq.com/monitors#/create
[5]: http://docs.datadoghq.com/help/
[6]: https://www.datadoghq.com/blog/
