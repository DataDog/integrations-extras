# Agent Check: chrony

## Overview

This check monitors [chrony][1].

The check executes `chronyc tracking` command and parses the output to extract key time synchronization metrics. It's designed to monitor the health and performance of chrony NTP service.

## Setup

### Installation

To install the chrony check for development testing:

1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/python/)
 on any machine.
2. Run `ddev release build chrony` to build the package.
3. [Download the Datadog Agent][2].
4. Upload the build artifact to a host with an Agent and run:
   `datadog-agent integration install -w path/to/chrony/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Ensure `chronyc` is installed on the host where the Agent runs (the check executes `chronyc tracking`).
2. Create the Agent configuration file:
   - Linux: `/etc/datadog-agent/conf.d/chrony.d/conf.yaml`
   - macOS (developer mode): `/opt/datadog-agent/etc/conf.d/chrony.d/conf.yaml`
3. Minimal config example:
   ```
   init_config:

   instances:
     - {}
   ```
4. For additional options, see the example config: [conf.yaml.example][4].

### Validation

Run the Agent check to verify it collects metrics:

```
datadog-agent check chrony
```

You should see the service check `chrony.can_connect` report `OK` when the `chronyc` command executes successfully.

## Data Collected

### Metrics

- **`chrony.stratum`**: NTP stratum level (unitless)
- **`chrony.systime`**: System time offset from NTP time (seconds)
- **`chrony.frequency`**: Frequency offset (unitless, ppm)
- **`chrony.residualfreq`**: Residual frequency (unitless, ppm)
- **`chrony.skew`**: Skew (unitless, ppm)
- **`chrony.rootdelay`**: Root delay (seconds)
- **`chrony.rootdispersion`**: Root dispersion (seconds)

## Service Checks

- **`chrony.can_connect`**: Returns `OK` if chronyc command executes successfully, `CRITICAL` otherwise

### Events

chrony does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://chrony-project.org
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/
[4]: https://github.com/DataDog/integrations-extras/blob/master/chrony/datadog_checks/chrony/data/conf.yaml.example

