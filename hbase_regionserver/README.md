# Hbase_regionserver Integration

## Overview

Get metrics from Hbase_regionserver service in real time to:

* Visualize and monitor Hbase_regionserver states.
* Be notified about Hbase_regionserver failovers and events.

## Setup

The Hbase_regionserver check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Hbase_regionserver check on your host:

1. [Download the Datadog Agent][1].
2. Download the [`check.py` file][2] for Hbase_regionserver.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `hbase_regionserver.py`.

### Configuration

To configure the Hbase_regionserver check: 

1. Create a `hbase_regionserver.d/` folder in the `conf.d/` folder at the root of your Agent's directory. 
2. Create a `conf.yaml` file in the `hbase_regionserver.d/` folder previously created.
3. Consult the [sample hbase_regionserver.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `hbase_regionserver` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The Hbase_regionserver check does not include any events at this time.

### Service Checks
The Hbase_regionserver check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/metadata.csv
[6]: http://docs.datadoghq.com/help/