# Agent Check: Redis Cloud

## Overview

Redis is a versatile and fast data store that supports strings, hashes, lists, sets, streams, and more. It also offers programmability, extensibility, persistence, clustering, and high availability features, as well as Redis Stack for modern data models and processing engines. 

The [Redis Cloud][1] integration is intended for use with Redis CLoud deployments of Redis software. It is not for use with Redis Enterprise installations, for that see the separate Redis Enterprise integration.

This integration provides metrics for databases, nodes, and shards), making it easier to detect problems before they become critical. 

## Setup

### Installation

1. Run the following command to install the Agent integration:
   ```shell
   datadog-agent integration install -t datadog-redis_cloud==1.0.0
   ```
   
2. Configure the integration by setting the `openmetrics_endpoint` to your cluster's master node. See [Getting Started with Integrations][2] for mor information.

3. [Restart][3] the Agent.


### Configuration

Set the `openmetrics_endpoint` to point to your cluster. For an example, see the [`conf.yaml.example` file][4].


### Validation

1. Ensure you can ping the machine, particularly in a cloud environment. Run `wget --no-check-certificate <endpoint>` or `curl -k <endpoint>` to ensure that you can receive metrics.

2. Check the [status][5] of the Datadog Agent.


## Data Collected

The current release gathers all metrics for databases, nodes, and shard.


### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.


### Service Checks

Redis Cloud does not include any service checks.


### Events

Redis Cloud does not include any events.


## Troubleshooting

Need help? Contact [Redis Field Engineering][7].

[1]: https://redis.io/docs/latest/operate/rc/
[2]: https://docs.datadoghq.com/getting_started/integrations/
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[4]: https://github.com/DataDog/integrations-extras/blob/master/redis_cloud/datadog_checks/redis_cloud/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/redis_cloud/metadata.csv
[7]: mailto:field.engineers@redis.com
