# Gnatsd_streaming Integration

## Overview

Get metrics from gnatsd_streaming service in real time to:

* Visualize and monitor gnatsd_streaming states
* Be notified about gnatsd_streaming failovers and events.

## Setup
### Installation

Install the `dd-check-gnatsd_streaming` package manually or with your favorite configuration manager

### Configuration

Edit the `gnatsd_streaming.yaml` file to point to your server and port, set the masters to monitor

You can change the number of channels returned in a single HTTP request with the `pagination` parameter
in the conf.yaml file.

### Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        gnatsd_streaming
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The gnatsd_streaming check is compatible with all major platforms

## Data Collected
### Metrics

See [metadata.csv](https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv) for a list of metrics provided by this integration.

Nats Streaming Server metrics are tagged with names like "nss-cluster_id"

### Events
The gnatsd_streaming check includes no events at this time

### Service Checks
This gnatsd_streaming check tags all service checks it collects with:

  * `nameserver:<nameserver_in_yaml>`
  * `resolved_hostname:<hostname_in_yaml>`

`gnatsd_streaming.can_resolve`:
Returns CRITICAL if the Agent fails to resolve the request, otherwise returns UP.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading
Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/)
