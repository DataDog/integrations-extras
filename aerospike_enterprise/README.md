# Agent Check: aerospike

## Overview

This check monitors [aerospike][1].

Fetch metrics from Aerospike Database in real time to:

- Visualize and monitor Aerospike stats and configs.

NOTE: Supports both Community Edition and Enterprise Edition, however few features and metrics are not availale in Community Edition

## Setup

NOTE: This Aerospike custom check is suggested to use for Aerospike Server version 7.0 and above. 
NOTE: This may work with older Aerospike Server versions, but some metrics / stats will be missing.

### Installation

The Aerospike check is included in the [Datadog Integration Extras][2] package.

To install the aerospike check on your host:

TODO: <FILL-IN-DETAILED-STEPS>

### Configuration

Below are the pre-requisites to configure and use Aerospike check for an Agent running on a host:

1. Install and configured the [Aerospike Prometheus Exporter][10]- refer to [Aerospike's documentation][11] for more details.

2. Edit the `aerospike.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Aerospike performance data. See the [sample aerospike.d/conf.yaml][4] for all available configuration options.

3. [Restart the Agent][5].

### Validation

We can check if the Aerospike check is correctly configured and working, use below command
"datadog-agent check aerospike" - Refer to [Run Agent Status subcommand][6]

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
[4]: https://github.com/DataDog/integrations-extras/blob/master/aerospike/datadog_checks/aerospike/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/aerospike/metadata.csv
[8]: https://aerospike.com/docs/database/reference/metrics
[9]: https://aerospike.com/docs/database/reference/config
[10]: https://github.com/aerospike/aerospike-prometheus-exporter
[11]: https://aerospike.com/docs/database/observe/monitor/components/
