# Agent Check: Aerospike Enterprise

## Overview

Aerospike Enterprise can push various metrics into Datadog so you can:

- Visualize key [Aerospike][1] metrics.
- Correlate overall Aerospike performance with the rest of your applications.

The integration includes dedicated dashboards that enable you to view Aerospike health and performance metrics. You can monitor throughput metrics, track the average latency of read/write operations over time, and create monitors that alert you on various critical metrics.

NOTE: Supports both Community Edition 7.0 and Enterprise Edition 7.0, however few features and metrics are not availale in Community Edition
NOTE: This may work with older Aerospike Server versions, but some metrics / stats will be missing.

## Setup

### Installation

The Aerospike check is included in the [Datadog Integration Extras][2] package.

To install the Aerospike enterprise check on your host:

1. Run the following command to install the integration [Community Integration] [12]:

- For the Datadog Agent v7+:
   ```shell
   agent integration install -t datadog-aerospike_enterprise==1.1.0
   ```

### Configuration

Below are the pre-requisites to configure and use Aerospike check for an Agent running on a host:

1. Install and configured the [Aerospike Prometheus Exporter][10]- refer to [Aerospike's documentation][11] for more details.

2. Edit the `aerospike_enterprise.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Aerospike performance data. See the [sample aerospike_enterprise.d/conf.yaml][4] for all available configuration options.

3. [Restart the Agent][5].

### Validation

We can check if the Aerospike check is correctly configured and working, use below command
"datadog-agent check aerospike_enterprise" - Refer to [Run Agent Status subcommand][6]

## Data Collected

### Metrics

See [Aerospike Metrics][8] or [Aerospike Configs][9] for a list of metrics and configurations provided by this integration.

### Events

Aerospike does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://aerospike.com
[2]: https://github.com/aerospike/datadog-integrations-extras/
[3]: https://aerospike.com
[4]: https://github.com/DataDog/integrations-extras/blob/master/aerospike_enterprise/datadog_checks/aerospike_enterprise/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/aerospike/metadata.csv
[8]: https://aerospike.com/docs/database/reference/metrics
[9]: https://aerospike.com/docs/database/reference/config
[10]: https://github.com/aerospike/aerospike-prometheus-exporter
[11]: https://aerospike.com/docs/database/observe/monitor/components/
[12]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
