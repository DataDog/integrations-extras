# Agent Check: Redis Enterprise

## Overview

The [Redis Enterprise][1] integration provides metrics for three critical aspects of a cluster; database, node, and shard. This integration enables fine-grained reporting that makes it easier to detect problems before they become critical. For a full list see the 'Metrics' section.


## Setup

### Installation

1. Run the following command to install the Agent integration:
   ```shell
   datadog-agent integration install -t datadog-redis_enterprise==1.0
   ```
   
2. Configure the integration by setting the `openmetrics_endpoint` to your cluster's master node. See [Integration][2] for further information.

3. [Restart][3] the agent.


### Configuration

Set the `openmetrics_endpoint` to point to your cluster. See the [example][4].


### Validation

1. Ensure you can ping the machine, particularly in a cloud environment. Run `wget --no-check-certificate <endpoint>` or `curl -k <endpoint>` to ensure that you can receive metrics.

2. Check the [status][5] of the Datadog agent.


## Data Collected

The current release gathers all metrics for databases, nodes, and shard.


### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.


### Service Checks

Redis Enterprise does not include any service checks.


### Events

Redis Enterprise does not include any events.


## Troubleshooting

Need help? Contact [Redis Field Engineering][7].

[1]: https://redis.com/redis-enterprise-software/overview/
[2]: https://docs.datadoghq.com/getting_started/integrations/
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[4]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise/datadog_checks/redis_enterprise/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise/metadata.csv
[7]: mailto:field.engineers@redis.com

