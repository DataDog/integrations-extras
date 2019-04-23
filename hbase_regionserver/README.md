# HBase RegionServer Integration

## Overview

Get metrics from the HBase RegionServer service in real time to:

* Visualize and monitor HBase RegionServer states.
* Be notified about HBase RegionServer failovers and events.

## Setup

The HBase RegionServer check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the HBase RegionServer check on your host:

1. [Download the Datadog Agent][1].
2. Create a `hbase_regionserver.d/` folder in the `conf.d/` folder at the root of your Agent's directory. 
3. Create a `conf.yaml` file in the `hbase_regionserver.d/` folder previously created.
4. Consult the [sample hbase_regionserver.yaml][2] file and copy its content in the `conf.yaml` file.
5. [Restart the Agent][3].

### Configuration

To configure the HBase RegionServer check: 

1. Open the `conf.yaml` file created during installation.
2. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
3. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `hbase_regionserver` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The HBase RegionServer check does not include any events.

### Service Checks
The HBase RegionServer check does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/metadata.csv
[6]: http://docs.datadoghq.com/help/
