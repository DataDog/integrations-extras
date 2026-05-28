# Agent Check: Linux PSI

## Overview

This check monitors Linux kernel **PSI (Pressure Stall Information)** through the Datadog Agent. PSI is the canonical "everything is slow" diagnostic for modern Linux: it answers *how much real work is being delayed by contention?* rather than the less useful *how busy is the CPU?*.

PSI exposes three files under `/proc/pressure/`:

- `cpu` - time spent stalled on CPU
- `memory` - time spent stalled on memory (allocation, swap, page reclaim)
- `io` - time spent stalled on block I/O

Each file has two metrics:

- `some` - at least one task was stalled at some point in the interval
- `full` - **all** tasks were stalled at some point (severe contention)

PSI is available on Linux kernel **4.20+** (December 2018). Some distributions require the `psi=1` boot parameter to enable it.

## Setup

The Linux PSI check is included in the [Datadog Agent][1] package, but is **not** enabled by default. To enable it, edit the configuration file as shown below.

### Installation

#### Host

Follow the instructions below to install this check on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] guide.

1. Verify PSI is enabled on the host:

   ```
   cat /proc/pressure/cpu
   ```

   If the file exists and shows two lines (one starting with `some`, one with `full`), PSI is enabled. If the directory is missing, your kernel either predates 4.20 or has PSI disabled. Add `psi=1` to your kernel command line (`/etc/default/grub` then `update-grub`) and reboot.

2. Run the Datadog Agent installer for your platform: [Linux instructions][3].

3. Create a `linux_psi.d/conf.yaml` file in the Agent's configuration directory (typically `/etc/datadog-agent/conf.d/`):

   ```yaml
   init_config:

   instances:
     - {}
   ```

   No required parameters; the check reads `/proc/pressure/*` directly.

4. [Restart the Agent][4].

#### Containerized

For containerized Agents (Docker, Kubernetes), mount the host's `/proc` into the Agent container at `/host/proc` and set the Agent's `procfs_path` config to `/host/proc`. This is the standard pattern for any check that reads host `/proc/*`.

### Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `tags` | list of strings | (none) | Tags attached to every metric and service check from this instance |
| `service` | string | (none) | Sets the `service:<value>` tag |
| `min_collection_interval` | number | 15 | Seconds between collection runs |

## Data Collected

### Metrics

See [`metadata.csv`](metadata.csv) for the complete list.

| Family | Metric | Type | Description |
|---|---|---|---|
| CPU | `system.pressure.cpu.some.{avg10,avg60,avg300}` | gauge (%) | % of wall time at least one task stalled on CPU over the 10/60/300s window |
| CPU | `system.pressure.cpu.some.total` | count (microseconds) | Cumulative stall time since boot |
| CPU | `system.pressure.cpu.full.*` | gauge / count | All-tasks-stalled CPU (kernel 5.13+ only) |
| Memory | `system.pressure.memory.some.{avg10,avg60,avg300,total}` | gauge / count | Memory pressure (some) |
| Memory | `system.pressure.memory.full.{avg10,avg60,avg300,total}` | gauge / count | Memory pressure (full) |
| I/O | `system.pressure.io.some.{avg10,avg60,avg300,total}` | gauge / count | I/O pressure (some) |
| I/O | `system.pressure.io.full.{avg10,avg60,avg300,total}` | gauge / count | I/O pressure (full) |

24 metrics total, gracefully degrading on older kernels that lack `/proc/pressure/cpu`'s `full` line.

### Service Checks

| Name | Description |
|---|---|
| `linux_psi.can_read` | `OK` when at least one PSI file was read successfully; `WARNING` when PSI is not enabled on the kernel; `CRITICAL` on permission errors |

### Events

This check does not emit events.

## Troubleshooting

### `linux_psi.can_read` is WARNING with "PSI not enabled"

Your kernel either predates 4.20 or PSI is disabled at boot. To check kernel version:

```
uname -r
```

To enable PSI on a kernel that supports it but disabled it by default, add `psi=1` to the kernel command line and reboot. On most distros this means editing `/etc/default/grub`:

```
GRUB_CMDLINE_LINUX_DEFAULT="... psi=1"
```

then `sudo update-grub && sudo reboot`.

### `linux_psi.can_read` is CRITICAL with "Permission denied"

`/proc/pressure/*` files are typically world-readable. If the Datadog Agent runs as a non-root user inside a restricted environment (selinux, apparmor, container with `/proc` masked), confirm read permission with:

```
sudo -u dd-agent cat /proc/pressure/cpu
```

For containerized Agents, ensure the host's `/proc` is mounted into the container (`-v /proc:/host/proc:ro`) and `procfs_path: /host/proc` is set in the Agent config.

### cgroup-scoped PSI

This version of the check reads system-wide PSI only. Per-cgroup PSI (`/sys/fs/cgroup/.../cpu.pressure`, etc.) is planned for a future release - track [issue link to be filed] for progress.

### Agent fails to load with `yaml: cannot unmarshal !!map into string`

The Agent log shows something like:

```
Error: could not load linux_psi:
* Python Check Loader: could not configure check instance for python check linux_psi: yaml: unmarshal errors:
  line 6: cannot unmarshal !!map into string
  line 7: cannot unmarshal !!map into string
```

This means a field in `conf.yaml` is a YAML map (nested dict) but the Agent expects a plain string. By far the most common cause is writing the `tags` block with the colon as a YAML separator instead of as part of the tag string:

```yaml
# WRONG - each entry becomes a {key: value} map
tags:
  - env: prod
  - region: eu-east-1

# CORRECT - each entry is a single string in `key:value` form
tags:
  - env:prod
  - region:eu-east-1
```

The same shape applies to any other string-typed field (`service`, `min_collection_interval`, etc.). If a field's documentation comment says `string`, it must be a single-line scalar, never a nested map.

To catch this before the Agent does, lint the file standalone with Python:

```
python3 -c "import yaml, pprint; pprint.pprint(yaml.safe_load(open('/etc/datadog-agent/conf.d/linux_psi.d/conf.yaml')))"
```

The `tags:` value should print as a list of strings (`['env:prod', ...]`), not a list of dicts (`[{'env': 'prod'}, ...]`).

### Check loads but no PSI metrics appear in Datadog

Confirm the Agent is running the check and seeing metrics locally:

```
sudo -u dd-agent datadog-agent check linux_psi
```

The command runs one check iteration in the foreground and prints every metric it would have submitted. You should see 24 `system.pressure.*` entries plus an OK `linux_psi.can_read` service check. If you see them locally but not in your Datadog account, the issue is upstream (Agent API key, network egress, account routing) and outside this integration's scope.

## Compatibility

| Requirement | Minimum |
|---|---|
| Linux kernel | 4.20 (Dec 2018) |
| Linux kernel for `cpu.full.*` metrics | 5.13 (May 2021) |
| Datadog Agent | 7.53 |
| Boot parameter `psi=1` | Required on distros that disable PSI by default |

The `system.pressure.cpu.full.*` metrics are not emitted on kernels older than 5.13; the rest of the metrics are emitted as long as `/proc/pressure/` exists. The check degrades gracefully without raising errors when individual files are missing or unreadable.

## Support

This integration is community-maintained by [@voseghale][7] and licensed under BSD-3-Clause matching the parent repo's `LICENSE` file. For bugs and feature requests, open an issue at the [integrations-extras repo][5] referencing the `linux_psi` integration. Pull requests are welcome - please open an issue first to discuss non-trivial changes. For general Datadog Agent support, contact [Datadog support][6].

[1]: https://app.datadoghq.com/account/settings/agent/latest
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://app.datadoghq.com/account/settings/agent/latest?platform=overview
[4]: https://docs.datadoghq.com/agent/configuration/agent-commands/#restart-the-agent
[5]: https://github.com/DataDog/integrations-extras
[6]: https://docs.datadoghq.com/help/
[7]: https://github.com/voseghale
