# Agent Check: Resin

## Overview

This check monitors [Resin][1] through the Datadog Agent.

## Setup

### Installation

The Resin check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Configure the [resin default server](https://www.caucho.com/resin-4.0/admin/cluster-server.xtp#JVMparameters:settingtheJVMcommandline) to enable JMX by adding the following JVM arguments:

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

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Service Checks

**resin.can_connect**:

Returns `CRITICAL` if the Agent is unable to connect to and collect metrics from the monitored Resin instance. Returns `OK` otherwise.

### Events

Resin does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://caucho.com/
[2]: https://github.com/DataDog/integrations-core/blob/master/resin/datadog_checks/resin/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[5]: https://docs.datadoghq.com/help
[6]: https://github.com/DataDog/integrations-extras/blob/master/resin/metadata.csv
