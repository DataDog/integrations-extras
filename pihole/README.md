# Agent Check: pihole

## Overview

This check monitors [Pi-hole][1] through the Datadog Agent.

## Setup

This package is **NOT** included in the [Datadog Agent][2] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Pi-hole check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior to version 6.8][4] or the [Docker Agent][5]:

1. [Download the Datadog Agent][2].

2. Run the following command to install the integrations wheel with the Agent:

   ```shell
      datadog-agent integration install -t datadog-pihole==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `pihole.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Pi-hole performance data. See the [sample pihole.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `pihole` under the Checks section.


### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Service Checks

**`pihole.running`**:

Returns `CRITICAL` if the Agent cannot communicate with the target host. Returns `OK` if the connection to Pi-hole is successful.

### Events

Pi-hole does not include any events.

### Log Collection

Enable logs collection for Datadog Agent in `/etc/datadog-agent/datadog.yaml` on Linux platforms. On other platforms, refer to the [Agent Configuration Files guide][11] for the location of your configuration file:

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

## Troubleshooting


Need help? Contact [Datadog support][12].

[1]: https://pi-hole.net/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/pihole/datadog_checks/pihole/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/pihole/metadata.csv
[11]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/
[11]: https://docs.datadoghq.com/help/
