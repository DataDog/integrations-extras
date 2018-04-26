# UPSC Stats Collector Integration

## Overview

Get metrics from UPSD service via upsc in real time to:

* Visualize and monitor UPS battery health and states
* Be notified about UPS failovers and events.

## Setup
### Configuration

Edit the `upsc.yaml` file to point to your server and port, set the masters to monitor

### Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        upsc
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The UPSC check is compatible with linux-based platforms.

## Data Collected
### Metrics
See [metadata.csv][1] for a list of metrics provided by this integration.

### Events
Push UPS failovers and events into your [Datadog Even Stream][2] 

### Service Checks
The UPSD check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][4].

[1]: https://github.com/DataDog/integrations-extras/blob/master/upsc/metadata.csv
[2]: https://docs.datadoghq.com/graphing/event_stream/
[3]: http://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/
