# Agent Check: Trino

## Overview

This check collects [Trino][1] metrics, such as the following examples:

- Overall activity metrics: completed/failed queries, data input/output size, execution time.
- Performance metrics: cluster memory, input CPU, execution CPU time.

## Setup

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Trino check on your host. See [Use Community Integrations][2] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-trino==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][9].

### Configuration

1. Edit the `trino.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory, to start collecting your Trino performance data.
   See the [sample trino.d/conf.yaml][3] for all available configuration options.

   This check has a limit of 350 metrics per instance. The number of returned metrics is indicated when running the Datadog Agent [status command][4].
   You can specify the metrics you are interested in by editing the [configuration][3].
   To learn how to customize the metrics to collect, read  [JMX Checks][5].
   If you need to monitor more metrics, contact [Datadog support][6].

2. [Restart the Agent][7]

### Validation

[Run the Agent's `status` subcommand][4] and look for Trino under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.

### Events

The Trino integration does not include any events.

### Service Checks

The Trino integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][6].


[1]: https://trino.io/
[2]: https://docs.datadoghq.com/agent/guide/use-community-integrations
[3]: https://github.com/DataDog/integrations-core/blob/master/jmx/datadog_checks/jmx/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/integrations/java/
[6]: https://docs.datadoghq.com/help/
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[8]: https://github.com/DataDog/integrations-extras/blob/master/trino/metadata.csv
[9]: https://docs.datadoghq.com/getting_started/integrations/
