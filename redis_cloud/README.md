# Agent Check: Redis Cloud

## Overview

Redis is a fast, versatile data store that supports a variety of data structures, including strings, hashes, lists, sets, streams, and more. It also offers programmability, extensibility, persistence, clustering, and high availability. The community edition of Redis adds additional data models and capabilities, which include vector search, probabilistic data structures, JSON support, and full-text search.

The [Redis Cloud][1] integration is intended for use with Redis Cloud deployments of Redis software. It is not for use with Redis Enterprise installations. For [Redis Enterprise][2], see the [Datadog Redis Enterprise integration][3].

The integration provides metrics for three critical cluster components: databases, nodes, and shards, via a Datadog Agent. This allows you to monitor database throughput, memory utilization, CPU usage, connection counts, replication health, and a variety of additional metrics within Datadog.
You can use this information to understand the overall health of your Redis Cloud clusters, diagnose application performance issues, and prevent downtime.

For a full list of supported metrics, see the **Metrics** section below.

## Setup

### Installation

1. Run the following command to install the Agent integration:
 - in Datadog v6
   ```shell
   datadog-agent integration install -t datadog-redis_cloud==1.0.0
   ```
 - in Datadog v7   
   ```shell
   agent integration install -t datadog-redis_cloud==1.0.0
   ```
   
2. Configure the integration by setting the `openmetrics_endpoint` to your cluster's master node. See [Getting Started with Integrations][4] for more information.

3. [Restart][5] the Agent.


### Configuration

Set the `openmetrics_endpoint` to point to your cluster. For an example, see the [`conf.yaml.example` file][6].


### Validation

1. Ensure you can ping the machine, particularly in a cloud environment. Run `wget --no-check-certificate <endpoint>` or `curl -k <endpoint>` to ensure that you can receive metrics.

2. Check the [status][7] of the Datadog Agent.


## Data Collected

The current release gathers all metrics for databases, nodes, and shard.


### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.


### Service Checks

Redis Cloud does not include any service checks.


### Events

Redis Cloud does not include any events.


## Troubleshooting

Need help? Contact [Redis Field Engineering][9].

[1]: https://redis.io/docs/latest/operate/rc/
[2]: https://redis.io/docs/latest/operate/rs/
[3]: https://app.datadoghq.com/integrations?integrationId=redis-enterprise
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://github.com/DataDog/integrations-extras/blob/master/redis_cloud/datadog_checks/redis_cloud/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/redis_cloud/metadata.csv
[9]: mailto:support@redis.com
