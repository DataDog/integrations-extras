# Hbase_master Integration

## Overview

Get metrics from hbase_master service in real time to:

* Visualize and monitor hbase_master states.
* Be notified about hbase_master failovers and events.

## Setup

### Configuration

Edit the `hbase_master.yaml` file to point to your server and port, set the masters to monitor.

### Validation

[Run the Agent's `status` subcommand][1] and look for `hbase_master` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events
The Hbase Master check does not include any events at this time.

### Service Checks
The Hbase Master check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][4].

[1]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[2]: https://github.com/DataDog/integrations-extras/blob/master/hbase_master/metadata.csv
[3]: http://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/
