# Redis Sentinel

## Overview

Get metrics from Redis's Sentinel service in real time to:

* Visualize and monitor sentinels states
* Be notified about failovers

## Setup

### Configuration

Edit the `redis_sentinel.yaml` file to point to your server and port, set the masters to monitor.

### Validation

[Run the Agent's `info` subcommand][1], you should see something like the following:

    Checks
    ======

        redis_sentinel
        --------------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The Redis Sentinel check is compatible with all major platforms.

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events
The Redis Sentinel check does not include any events at this time.

### Service Checks
The Redis Sentinel check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][4].

[1]: https://docs.datadoghq.com/agent/faq/agent-status-and-information/
[2]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/metadata.csv
[3]: http://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/
