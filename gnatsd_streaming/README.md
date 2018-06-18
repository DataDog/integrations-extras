# Gnatsd_streaming Integration

## Overview

Get metrics from gnatsd_streaming service in real time to:

* Visualize and monitor gnatsd_streaming states
* Be notified about gnatsd_streaming failovers and events.

## Setup

### Installation

To install the Gnatsd_streaming check on your host:

1. [Download the Datadog Agent][4].
2. Download the [`check.py` file][5] for Gnatsd_streaming.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `gnatsd_streaming.py`.


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

See [metadata.csv][1] for a list of metrics provided by this integration.

Nats Streaming Server metrics are tagged with names like "nss-cluster_id"

### Events

If you are running Nats Streaming Server in a Fault Tolerant group a Nats Streaming Failover event will be issued
when the status of a Server changes between `FT_STANDBY` and `FT_ACTIVE`

### Service Checks
This gnatsd_streaming check tags all service checks it collects with:

  * `server_name:<server_name_in_yaml>`
  * `url:<host_in_yaml>`

`gnatsd_streaming.can_connect`:
Returns `CRITICAL` if the Agent fails to receive a 200 from the _monitoring_ endpoint, otherwise returns `OK`.

## Troubleshooting
Need help? Contact [Datadog Support][2].

## Further Reading
Learn more about infrastructure monitoring and all our integrations on [our blog][3]


[1]: https://github.com/DataDog/datadog-sdk-testing/blob/master/lib/config/metadata.csv
[2]: http://docs.datadoghq.com/help/
[3]: https://www.datadoghq.com/blog/
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://github.com/DataDog/integrations-extras/blob/master/gnatsd_streaming/check.py
