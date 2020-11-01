# Agent Check: flume

## Overview

This check monitors [flume][1].

## Setup

### Installation

To install the flume check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build flume` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/flume/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Configure the flume agent to enable JMX by adding the following JVM arguments to your [flume-env.sh](https://flume.apache.org/FlumeUserGuide.html#jmx-reporting): 

```
export JAVA_OPTS=”-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=5445 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false”

```

2. Edit the `flume.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your flume performance data.
   See the [sample flume.d/conf.yaml][2] for all available configuration options.

   This check has a limit of 350 metrics per instance. The number of returned metrics is indicated in the info page.
   You can specify the metrics you are interested in by editing the configuration below.
   To learn how to customize the metrics to collect visit the [JMX Checks documentation][3] for more detailed instructions.
   If you need to monitor more metrics, contact [Datadog support][4].

2. [Restart the Agent][5]

### Validation

[Run the Agent's `status` subcommand][6] and look for `flume` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Service Checks

**flume.can_connect**:

Returns `CRITICAL` if the Agent is unable to connect to and collect metrics from the monitored Flume instance. Returns `OK` otherwise.

### Events

flume does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][4].


[1]: https://flume.apache.org/
[2]: https://github.com/DataDog/integrations-extras/blob/master/flume/datadog_checks/flume/data/conf.yaml.example
[3]: https://docs.datadoghq.com/integrations/java/
[4]: https://docs.datadoghq.com/help/
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/flume/metadata.csv