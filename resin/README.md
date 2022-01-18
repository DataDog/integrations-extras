# Agent Check: Resin

## Overview

This check monitors [Resin][1] through the Datadog Agent.

## Setup

### Installation

The Resin check is not included in the [Datadog Agent][2] package, so you need to install it.

### Configuration

1. Configure the [resin default server][9] to enable JMX by adding the following JVM arguments:

```
<server-default>
  <jvm-arg>-Dcom.sun.management.jmxremote</jvm-arg>
  <jvm-arg>-Dcom.sun.management.jmxremote.port=7199</jvm-arg>
</server-default>
```

2. Edit the `resin.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your resin performance data. See the [sample resin.d/conf.yaml][2] for all available configuration options.

3. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `resin` under the Checks section.

### Log collection

Enable logs collection for Datadog Agent in `/etc/datadog-agent/datadog.yaml` on Linux platforms. On other platforms, see the [Agent Configuration Files guide][6] for the location of your configuration file:

```yaml
logs_enabled: true
```

- Enable this configuration block to your `resin.d/conf.yaml` file to start collecting Logs:
    ```yaml
    logs:
      - type: file
        path: /var/opt/resin/log/*.log
        source: resin
    ```

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this integration.

### Events

Resin does not include any events.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][7].


[1]: https://caucho.com/
[2]: https://github.com/DataDog/integrations-extras/tree/master/resin
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/resin/metadata.csv
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/
[7]: https://docs.datadoghq.com/help/
[8]: https://github.com/DataDog/integrations-extras/blob/master/resin/assets/service_checks.json
[9]: https://www.caucho.com/resin-4.0/admin/cluster-server.xtp#JVMparameters:settingtheJVMcommandline
