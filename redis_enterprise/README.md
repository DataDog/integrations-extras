# Agent Check: Redis Enterprise

## Overview

Redis is a fast, versatile data store that supports a variety of data structures, including strings, hashes, lists, sets, streams, and more. It also offers programmability, extensibility, persistence, clustering, and high availability. The community edition of Redis adds additional data models and capabilities, which include vector search, probabilistic data structures, JSON support, and full-text search.

This integration works with on-premsises and private cloud installations of [Redis Enterprise][1]. The integration provides metrics for three critical cluster components: databases, nodes, and shards. An overview dashboard is also included.

For a full list of supported metrics, see the **Metrics** section below.

## Setup

### Installation

1. Run the following command to install the Agent integration:
   ```shell
   datadog-agent integration install -t datadog-redis_enterprise==1.0.0
   ```
   
2. Configure the integration by setting the `openmetrics_endpoint` to your cluster's master node. See [Integration][2] for further information.

3. [Restart][3] the agent.


### Configuration

Set the `openmetrics_endpoint` to point to your cluster. See the [example][4].


### Validation

1. Ensure you can ping the machine, particularly in a cloud environment. Run `wget --no-check-certificate <endpoint>` or `curl -k <endpoint>` to ensure that you can receive metrics.

2. Check the [status][5] of the Datadog agent.


## Data Collected

The current release gathers all metrics for databases, nodes, and shards.


### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.


### Service Checks

Redis Enterprise does not include any service checks.


### Events

Redis Enterprise does not include any events.


## Troubleshooting

Need help? Please contact [Redis Support][8].

[1]: https://redis.com/redis-enterprise-software/overview/
[2]: https://docs.datadoghq.com/getting_started/integrations/
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[4]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise/datadog_checks/redis_enterprise/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise/metadata.csv
[7]: mailto:field.engineers@redis.com
[8]: https://redis.io/support/
