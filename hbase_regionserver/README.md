# Hbase_regionserver Integration

## Overview

Get metrics from hbase_regionserver service in real time to:

* Visualize and monitor hbase_regionserver states.
* Be notified about hbase_regionserver failovers and events.

## Setup
### Installation

Install the `dd-check-hbase_regionserver` package manually or with your favorite configuration manager.

### Configuration

Edit the `hbase_regionserver.yaml` file to point to your server and port, set the masters to monitor.

### Validation

[Run the Agent's `info` subcommand](https://docs.datadoghq.com/agent/faq/agent-status-and-information/), you should see something like the following:

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
See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/metadata.csv) for a list of metrics provided by this integration.

### Events
The Hbase Region Server check does not include any events at this time.

### Service Checks
The Hbase Region Server check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).