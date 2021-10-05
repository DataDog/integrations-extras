# Agent Check: Flume

## Overview

This check monitors [Apache Flume][1].

## Setup

The Flume check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Flume check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-flume==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Configure the Flume agent to enable JMX by adding the following JVM arguments to your [flume-env.sh][7]: 

```
export JAVA_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=5445 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false"

```

2. Edit the `flume.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting Flume performance data.
   See the [sample `flume.d/conf.yaml`][8] file for all available configuration options.

   This check has a limit of 350 metrics per instance. The number of returned metrics is indicated in the info page.
   You can specify the metrics you are interested in by editing the configuration below.
   To learn how to customize the metrics to collect visit the [JMX Checks documentation][9] for more detailed instructions.
   If you need to monitor more metrics, contact [Datadog support][10].

3. [Restart the Agent][11]

### Validation

[Run the Agent's `status` subcommand][12] and look for `flume` under the Checks section.

### Component metrics

The metrics retrieved by this check depend on the source, channel, and sink used by your Flume agent. For a full list of metrics exposed by each component, review [Available Component Metrics][11] from the Apache Flume documentation. For a list of the metrics that you can see in Datadog, see the [Metrics](#metrics) section on this page.

## Data Collected

### Metrics

See [metadata.csv][13] for a list of metrics provided by this check.

### Events

Flume does not include any events.

### Service Checks

See [service_checks.json][15] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][10].


[1]: https://flume.apache.org/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://flume.apache.org/FlumeUserGuide.html#jmx-reporting
[8]: https://github.com/DataDog/integrations-extras/blob/master/flume/datadog_checks/flume/data/conf.yaml.example
[9]: https://docs.datadoghq.com/integrations/java/
[10]: https://docs.datadoghq.com/help/
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[12]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[13]: https://github.com/DataDog/integrations-extras/blob/master/flume/metadata.csv
[14]: https://flume.apache.org/FlumeUserGuide.html#available-component-metrics
[15]: https://github.com/DataDog/integrations-extras/blob/master/flume/assets/service_checks.json
