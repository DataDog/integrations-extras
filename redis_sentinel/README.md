# Redis Sentinel

## Overview

Get metrics from Redis's Sentinel service in real time to:

* Visualize and monitor sentinels states
* Be notified about failovers


## Setup

The Redis's Sentinel check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Redis's Sentinel check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][1].
2. Download the [`redis_sentinel.py` file][8] for Redis Sentinel.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:

1. Install the [developer toolkit][7] on any machine.
2. Run `ddev release build redis_sentinel` to build the package.
3. [Download the Datadog Agent][1].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/redis_sentinel/dist/<ARTIFACT_NAME>.whl`.

**Note**: The `integration` command is only available for Agent 6.8+.

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
The Redis's Sentinel check does not include any events.

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
Need help? Contact [Datadog support][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/datadog_checks/redis_sentinel/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[8]: https://github.com/DataDog/integrations-extras/blob/master/redis_sentinel/datadog_checks/redis_sentinel/redis_sentinel.py
