# Hbase_master Integration

## Overview

Get metrics from Hbase_master service in real time to:

* Visualize and monitor Hbase_master states.
* Be notified about Hbase_master failovers and events.

## Setup

The Hbase_master check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Hbase_master check on your host:

1. [Download the Datadog Agent][1].
2. Download the [`check.py` file][2] for Hbase_master.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `hbase_master.py`.

### Configuration

To configure the Hbase_master check: 

1. Create a `hbase_master/` folder in the `conf.d/` folder at the root of your Agent's directory. 
2. Create a `conf.yaml` file in the `hbase_master/` folder previously created.
3. Consult the [sample hbase_master.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `hbase_master` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The Hbase_master check does not include any event at this time.

### Service Checks
The Hbase_master check does not include any service check at this time.

## Troubleshooting
Need help? Contact [Datadog Support][6].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][7]

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/hbase_master/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/hbase_master/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://www.datadoghq.com/blog/