# Hbase_master Integration

## Overview

Get metrics from Hbase_master service in real time to:

* Visualize and monitor Hbase_master states.
* Be notified about Hbase_master failovers and events.

### Installation

To install the Hbase_master check on your host:

1. [Download the Datadog Agent][1].
2. Create a `hbase_master.d/` folder in the `conf.d/` folder at the root of your Agent's directory. 
3. Create a `conf.yaml` file in the `hbase_master.d/` folder previously created.
4. Consult the [sample hbase_master.yaml][2] file and copy its content in the `conf.yaml` file.
5. [Restart the Agent][3].

### Configuration

To configure the Hbase_master check: 

1. Open the `conf.yaml` file created during installation.
2. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
3. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `hbase_master` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The Hbase_master check does not include any events at this time.

### Service Checks
The Hbase_master check does not include any service checks at this time.

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