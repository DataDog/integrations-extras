# Agent Check: Redis Enterprise

## Overview

Redis is a fast, versatile data store that supports a variety of data structures, including strings, hashes, lists, sets, streams, and more. It also offers programmability, extensibility, persistence, clustering, and high availability. The community edition of Redis adds additional data models and capabilities, which include vector search, probabilistic data structures, JSON support, and full-text search.

This integration works with on-premises and private cloud installations of [Redis Enterprise][1].
The integration provides metrics for three critical cluster components: databases, nodes, and shards. This allows you to monitor database throughput, memory utilization, CPU usage, connection counts, replication health, and a variety of additional metrics within Datadog.
You can use this information to understand the overall health of your Redis Enterprise clusters, diagnose application performance issues, and prevent downtime.

For a full list of supported metrics, see the [Metrics](#metrics) section below.

## Setup

### Installation

1. Run the following command to install the Agent integration:
   ```shell
   datadog-agent integration install -t datadog-redis_enterprise==1.1.0
   ```
   
2. Configure the integration by setting the `openmetrics_endpoint` to your cluster's master node. See [Integration][2] for further information.

3. [Restart][3] the agent.


### Configuration

Set the `openmetrics_endpoint` to point to your cluster. See the [example][4]. Leave `tls_verify` set to false.

There are two optional parameters: `extra_metrics` and `excluded_metrics`, as noted in the example configuration file.

The extra_metrics parameter takes a list of metric groups. The following are the available groups: RDSE.REPLICATION, 
RDSE.LISTENER, RDSE.PROXY, RDSE.BIGSTORE, RDSE.FLASH, RDSE.SHARDREPL. The default metrics groups RDSE.NODE, 
RDSE.DATABASE, and RDSE.SHARD are automatically inserted by the integration.

The exclude_metrics parameter takes a list of individual metrics to exclude, meaning that this information will not be 
passed on to Datadog. The individual metrics should be stripped of their prefix, e.g., 'rdse.bdb_up' would 
become 'bdb_up'. The full list of metrics is available on the 'Data Collected' tab of the integration page, or via the link in the [Metrics](#metrics) section. 
The following extra groups use the associated prefixes, which can be used to search for individual metrics on 
the data collected page.

| Group            | Prefix                      | Notes                                                |
|------------------|-----------------------------|------------------------------------------------------|
| RDSE.NODE        | rdse.node_                  | This will return bigstore and flash metrics as well  |
| RDSE.DATABASE    | rdse.bdb_                   | This will return replication metrics as well         |
| RDSE.SHARD       | rdse.redis_                 | This will return shard replication metrics as well   |
| RDSE.REPLICATION | rdse.bdb_crdt_              |                                                      |
| RDSE.REPLICATION | rdse.bdb_replicaof_         |                                                      |
| RDSE.SHARDREPL   | rdse.redis_crdt_            |                                                      |
| RDSE.PROXY       | rdse.dmcproxy_              |                                                      |
| RDSE.LISTENER    | rdse.listener_              |                                                      |
| RDSE.BIGSTORE    | rdse.node_bigstore_         |                                                      |
| RDSE.FLASH       | rdse.node_available_flash   | All flash metrics are of the form: rdse.node_*_flash |

### Validation

1. Ensure you can ping the machine, particularly in a cloud environment. Run `wget --no-check-certificate <endpoint>` 
or `curl -k <endpoint>` to ensure that you can receive metrics.

2. Check the [status][5] of the Datadog agent.


## Data Collected

The current release gathers all metrics for databases, nodes, and shards. Optionally, via the extra_metrics parameter, 
data for replication, proxy, listener, etc. can be gathered; see the list in the [Configuration](#configuration) section.


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
