# Agent Check: neo4j

## Overview

[Neo4j][1] is an enterprise-strength graph database that combines native graph storage, advanced security, scalable speed-optimized architecture, and ACID compliance to ensure predictability and integrity of relationship-based queries. Neo4j stores and manages data in its more natural, connected state, maintaining data relationships that deliver lightning-fast queries, deeper context for analytics, and a pain-free modifiable data model.

Neo4j metrics enable database administrators to monitor their Neo4j deployments. DBAs want to understand the memory usage (heap and page cache), number of transactions, cluster status, database size (including number of nodes, relationsihps and properties), and query performance. 

With this integration, visualize important Neo4j metrics in our out-of-the-box dashboards and enable your DBAs to troubleshoot and monitor the health of your Neo4j databases.


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

2. Datadog listens on port 5000 for the dogstatsd_stats_port and expvar_port. In your neo4j.conf file, you will need to change the server.discovery.listen_address and the server.discovery.advertised_address to use a port other than 5000.

3. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `neo4j` under the Checks section.

## Data Collected

### Metrics

The integration collects metrics through the neo4j prometheus endpoint. Ensure your neo4j edition supports the prometheus endpoint.

**Neo4j Version 4**
Neo4j 4 metrics are collected as documented [here][11]. The most commonly monitored metrics are provided in the out-of-the-box dashboards. 

**Neo4j Version 5**
Neo4j 5 metrics are collected as documented [here][10]. The most commonly monitored metrics are provided in the out-of-the-box dashboards. 

Please note each version collects a different set of metrics. The versions are listed in the description of the metric.

See [metadata.csv][6] for the full list of metrics provided by this check.

### Service Checks

Service check `neo4j.prometheus.health` is submitted in the base check

### Events

Neo4j does not include any events.


## Troubleshooting

Need help? Contact [Neo4j support][7].

[1]: https://neo4j.com/
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/datadog_checks/neo4j/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/metadata.csv
[7]: mailto:support@neo4j.com
[8]: https://app.datadoghq.com/account/settings/agent/latest
[9]: https://neo4j.com/docs/upgrade-migration-guide/current/version-5/migration/install-and-configure/#_performance_metrics
[10]: https://neo4j.com/docs/operations-manual/5/monitoring/metrics/reference/
[11]: https://neo4j.com/docs/operations-manual/4.4/monitoring/metrics/reference/
[12]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7
