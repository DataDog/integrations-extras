# Gnatsd Integration

## Overview

Get metrics from gnatsd service in real time to:

* Visualize and monitor gnatsd states
* Be notified about gnatsd failovers and events.

## Setup

### Installation

To install the Gnatsd check on your host:

1. [Download the Datadog Agent][4].
2. Download the [`check.py` file][5] for Gnatsd.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `gnatsd.py`.

### Configuration

Edit the `gnatsd.yaml` file to point to your server and port, set the masters to monitor

* host: set to the gnatsd host to monitor
* port: set to the _monitoring_ port used by gnatsd
* tags: add these tags to recorded metrics
* server_name: set to what should be displayed in DataDog

### Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        gnatsd
        -----------
          - instance #0 [OK]
          - Collected 23 metrics, 0 events & 1 service checks

## Compatibility

The gnatsd check is compatible with all major platforms

## Data Collected
### Metrics

See [metadata.csv][1] for a list of metrics provided by this integration.

### Events
The gnatsd check does not include any events.

### Service Checks
This gnatsd check tags all service checks it collects with:

* `server_name:<server_name_in_yaml>`
* `url:<host_in_yaml>`

`gnatsd.can_connect`:
Returns `CRITICAL` if the Agent fails to receive a 200 from the _monitoring_ endpoint, otherwise returns `OK`.

## Troubleshooting
Need help? Contact [Datadog support][2].

[1]: https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv
[2]: http://docs.datadoghq.com/help/
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd/check.py
