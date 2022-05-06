# Agent Check: neo4j

## Overview

This check monitors [neo4j][1] through the Datadog Agent.
Please verify the metrics and checks that are submitted through this agent. Since Neo4j 4.0 and onward supports multiple databases, some metrics and checks are no longer published.

## Setup


Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the neo4j check on your host:

1. Download and install the [Datadog Agent][8].
2. To install the neo4j check on your host:

   ```shell
   datadog-agent integration install -t datadog-neo4j==<INTEGRATION_VERSION>
   ```


### Configuration

1. Edit the `neo4j.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your neo4j performance data. See the [sample neo4j.d/conf.yaml][3] for all available configuration options.

2. The neo4j_url has been replaced by host. Please ensure any updates use host.

3. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `neo4j` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

Service check `neo4j.prometheus.health` is submitted in the base check

### Events

neo4j does not include any events.

## Troubleshooting


Need help? Contact [Datadog support][7].

[1]: https://neo4j.com/
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/datadog_checks/neo4j/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/metadata.csv
[7]: https://docs.datadoghq.com/help
[8]: https://app.datadoghq.com/account/settings#agent
