# Agent Check: pihole

## Overview

This check monitors [Pi-hole][1] through the Datadog Agent.

## Setup

The Pi-hole check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Pi-hole check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   sudo -u dd-agent -- datadog-agent integration install -t datadog-pihole==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `pihole.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Pi-hole performance data. See the [sample pihole.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

Run the [Agent's status subcommand][9] and look for `pihole` under the Checks section.

### Log collection

Enable logs collection for Datadog Agent in `/etc/datadog-agent/datadog.yaml` on Linux platforms. On other platforms, see the [Agent Configuration Files guide][11] for the location of your configuration file:

```yaml
logs_enabled: true
```

- Enable this configuration block to your `pihole.d/conf.yaml` file to start collecting Logs:
    ```yaml
    logs:
      - type: file
        path: /var/log/pihole.log
        source: pihole
    ```

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Events

Pi-hole does not include any events.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].


[1]: https://pi-hole.net/
[2]: /account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/pihole/datadog_checks/pihole/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/pihole/metadata.csv
[11]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/pihole/assets/service_checks.json
