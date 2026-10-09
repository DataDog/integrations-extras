# Agent Check: exim

## Overview

This check monitors [Exim][1] through the Datadog Agent. It runs `exim -bp | exiqsumm` and reports the number and volume of queued messages per recipient domain.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][4] for guidance on applying these instructions.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the exim check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-exim==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][2].

### Prerequisites

The check runs `exim -bp` and pipes its output through `exiqsumm`, so both utilities must be installed on the host. The check uses the absolute paths `/usr/sbin/exim` and `/usr/sbin/exiqsumm` by default because the Agent's environment often does not have `/usr/sbin` in its `PATH`. Set `exim_path` and `exiqsumm_path` if your installation uses other locations.

#### Queue listing permissions

Exim only allows admin users to list the queue while the `queue_list_requires_admin` option is enabled, which is the default. Exim treats root, the Exim user, members of the Exim group and members of the groups in `admin_groups` as admin users. On a default installation `exim -bp` therefore fails for the Agent user and the check reports `exim.returns.output` as `CRITICAL` with the error from Exim:

- Exim 4.96 and earlier: `exim: permission denied`
- Exim 4.97 and later: `exim: permission denied; not admin`

Choose one of the following options:

- **Use sudo (recommended).** Set `use_sudo: true` in the check configuration. The check then runs `sudo -n /usr/sbin/exim -bp`, which fails immediately instead of prompting for a password when sudo is not set up. Grant the Agent user passwordless `sudo` for exactly this command by adding the following line to `/etc/sudoers` (for example with `visudo`). Adjust the path if you changed `exim_path`:

  ```text
  dd-agent ALL=(root) NOPASSWD:/usr/sbin/exim -bp
  ```

  On Red Hat based systems, also add:

  ```text
  Defaults:dd-agent !requiretty
  ```

  This is the narrowest option: the rule only allows listing the queue.

- **Add the Agent user to the Exim group.** For example `usermod -aG Debian-exim dd-agent` on Debian and Ubuntu, or `usermod -aG exim dd-agent` on Red Hat based systems, then restart the Agent. No sudo is needed, but Exim has no read-only admin role: the Agent user also gets every other admin privilege, such as removing, freezing or forcing delivery of queued messages.

- **Disable `queue_list_requires_admin`** in the Exim configuration. This lets any local user list the queue, including sender and recipient addresses, so only do this when that is acceptable for your environment.

### Configuration

1. Edit the `exim.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your exim performance data. See the [sample exim.d/conf.yaml][5] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - use_sudo: true
       ## Uncomment if the binaries are not in /usr/sbin
       # exim_path: /usr/sbin/exim
       # exiqsumm_path: /usr/sbin/exiqsumm
   ```

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `exim` under the Checks section. A healthy run reports `Metric Samples: Last Run: 2` or more and the `exim.returns.output` service check as `OK`.

`exiqsumm` always prints a `TOTAL` summary row, so the `exim.queue.count` and `exim.queue.volume` metrics with the tag `domain:TOTAL` are submitted on every successful run, with a value of `0` when the queue is empty. If these metrics are missing, the command did not run; check the service check message and the Agent log for the error reported by `exim` or `sudo`, such as `sudo: a password is required` when the sudoers rule is missing.

To verify the command outside the Agent, run it as the Agent user:

```shell
sudo -u dd-agent /bin/sh -c 'sudo -n /usr/sbin/exim -bp | /usr/sbin/exiqsumm'
```

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.

Metrics are tagged with `domain:<RECIPIENT_DOMAIN>`. The `domain:TOTAL` series summarizes the whole queue. Volumes are reported in bytes, converted from the `KB` and `MB` values that `exiqsumm` rounds to.

### Events

The Exim integration does not include any events.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][10].


[1]: https://www.exim.org/
[2]: https://docs.datadoghq.com/getting_started/integrations/
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/exim/datadog_checks/exim/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/exim/metadata.csv
[9]: https://github.com/DataDog/integrations-extras/blob/master/exim/assets/service_checks.json
[10]: https://docs.datadoghq.com/help/
