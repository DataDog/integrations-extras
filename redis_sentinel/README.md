# Redis Sentinel

## Overview

Get metrics from Redis's Sentinel service in real time to:

* Visualize and monitor sentinels states
* Be notified about failovers


## Setup

The Redis's Sentinel check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Redis's Sentinel check on your host:

1. [Download the Datadog Agent][1].
2. Download the [`check.py` file][2] for Redis's Sentinel.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `redis_sentinel.py`.

### Configuration

To configure the Redis's Sentinel check:

1. Create a `redis_sentinel.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `redis_sentinel.d/` folder previously created.
3. Consult the [sample redis_sentinel.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `redis_sentinel` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The Redis's Sentinel check does not include any events at this time.

### Service Checks
**`redis.sentinel.master_is_down`**

The check returns:

* `OK` if the master is up.
* `CRITICAL` if the master is down.


**`redis.sentinel.master_is_disconnected`**

The check returns:

* `OK` if the master is not disconnected.
* `CRITICAL` if the master is disconnected.


**`redis.sentinel.slave_master_link_down`**

The check returns:

* `OK` if the master link status is ok.
* `CRITICAL` if the master link status is not ok.


**`redis.sentinel.slave_is_disconnected`**

The check returns:

* `OK` if the slave is not disconnected.
* `CRITICAL` if the slave is disconnected.

## Troubleshooting
Need help? Contact [Datadog Support][6].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][7]

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://www.datadoghq.com/blog/
