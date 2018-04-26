# Hbase_regionserver Integration

## Overview

Get metrics from hbase_regionserver service in real time to:

* Visualize and monitor hbase_regionserver states.
* Be notified about hbase_regionserver failovers and events.

## Setup

### Configuration

Edit the `hbase_regionserver.yaml` file to point to your server and port, set the masters to monitor.

### Validation

[Run the Agent's `info` subcommand][1], you should see something like the following:

    Checks
    ======

        hbase_regionserver
        -----------
          - instance #0 [OK]
          - Collected 150 metrics, 0 events & 0 service checks

## Compatibility

The hbase_regionserver check is compatible with all major platforms.

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events
The Hbase Region Server check does not include any events at this time.

### Service Checks
The Hbase Region Server check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][4].

[1]: https://docs.datadoghq.com/agent/faq/agent-status-and-information/
[2]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/metadata.csv
[3]: http://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/
