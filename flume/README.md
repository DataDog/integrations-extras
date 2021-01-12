# Agent Check: Flume

## Overview

This check monitors [Apache Flume][1].

## Setup

### Installation

To install the Flume check on your host:

2. Run `ddev release build flume` to build the package.

3. [Download the Datadog Agent][3].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/flume/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Configure the Flume agent to enable JMX by adding the following JVM arguments to your [flume-env.sh][4]: 

```
export JAVA_OPTS=”-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=5445 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false”

```

2. Edit the `flume.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting Flume performance data.
   See the [sample `flume.d/conf.yaml`][5] file for all available configuration options.

   This check has a limit of 350 metrics per instance. The number of returned metrics is indicated in the info page.
   You can specify the metrics you are interested in by editing the configuration below.
   To learn how to customize the metrics to collect visit the [JMX Checks documentation][6] for more detailed instructions.
   If you need to monitor more metrics, contact [Datadog support][7].

3. [Restart the Agent][8]

### Validation

[Run the Agent's `status` subcommand][9] and look for `flume` under the Checks section.

### Component metrics

The metrics retrieved by this check depend on the source, channel, and sink used by your Flume agent. For a full list of metrics exposed by each component, review [Available Component Metrics][11] from the Apache Flume documentation. For a list of the metrics that you can see in Datadog, see the [Metrics](#metrics) section on this page.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Service Checks

**flume.can_connect**:

Returns `CRITICAL` if the Agent is unable to connect to and collect metrics from the monitored Flume instance. Returns `OK` otherwise.

### Events

Flume does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].


[1]: https://flume.apache.org/
[2]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://flume.apache.org/FlumeUserGuide.html#jmx-reporting
[5]: https://github.com/DataDog/integrations-extras/blob/master/flume/datadog_checks/flume/data/conf.yaml.example
[6]: https://docs.datadoghq.com/integrations/java/
[7]: https://docs.datadoghq.com/help/
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/flume/metadata.csv
[11]: https://flume.apache.org/FlumeUserGuide.html#available-component-metrics
