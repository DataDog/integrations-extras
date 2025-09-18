# Agent Check: Redis Enterprise Prometheus

## Overview

Redis is a high-performance data store that supports a variety of data structures, including strings, hashes, lists, sets, streams, and more. It provides programmability, extensibility, persistence, clustering, and high availability. The community edition extends Redis with vector search, probabilistic data structures, JSON support, and full-text search capabilities.

This integration works with on-premises and private cloud installations of [Redis Enterprise][1] using Prometheus metrics.
The integration provides metrics for four critical cluster components: clusters, databases, nodes, and shards. This allows you to monitor database throughput, memory utilization, CPU usage, connection counts, replication health, and a variety of additional metrics within Datadog. You can use this information to understand the overall health of your Redis Enterprise clusters, diagnose application performance issues, and prevent downtime.

For a full list of supported metrics, see the [Metrics](#metrics) section below.

### Redis Enterprise Compatibility

The Redis Enterprise Prometheus integration provides support for the [V2 Redis Enterprise Software Metrics][10] which are available in Redis Enterprise Software versions `7.8.0` and higher. For older versions of Redis Enterprise Software, you may use the [Redis Enterprise][11] integration.

## Setup

### Installation

1. Run the following command to install the Agent integration:
   ```shell
   datadog-agent integration install -t datadog-redis_enterprise_prometheus==1.0.0
   ```
    > **Note**: For containerized environments, see the [Datadog documentation page][9].
  
2. Configure the integration by setting the `openmetrics_endpoint` to your cluster's master node. See the [configuration](#configuration) section for more information.

3. [Restart][3] the agent.


### Configuration

Point the `openmetrics_endpoint` to your cluster and ensure `tls_verify` remains false (by default). Reference the [example config file][4] for guidance.

Two optional parameters are available, as shown in the example configuration file:

**`extra_metrics`** - Accepts a list of metric groups:
- Available groups: REDIS2.REPLICATION, REDIS2.SHARDREPL, REDIS2.LDAP, REDIS2.NETWORK, REDIS2.MEMORY, REDIS2.X509, REDIS2.DISK, REDIS2.FILESYSTEM, REDIS2.PROCESS, REDIS2.PRESSURE, REDIS2.FLASH, REDIS2.SEARCH
- Default groups (automatically included): RDSE2.REDIS_CLUSTER, RDSE2.REDIS_DATABASE, RDSE2.REDIS_SHARD, RDSE2.REDIS_INFO, RDSE2.REDIS_NODE

**`excluded_metrics`** - Accepts a list of individual metrics to exclude from Datadog:
- Remove the prefix when specifying metrics (for example, use `generation` instead of `rdse2.generation`).
- View the complete metrics list on the Data Collected tab of the integration tile.
- Use group prefixes to search for specific metrics on the data collected page.
The following groups use the associated prefixes, which can be used to search for individual metrics on 
the data collected page.

| Group                    | Prefix                      | Notes                                                |
|--------------------------|----------------------------|------------------------------------------------------|
| RDSE2.REDIS_CLUSTER      | rdse2.                     | Cluster-level metrics                               |
| RDSE2.REDIS_DATABASE     | rdse2.endpoint_            | Database endpoint metrics                           |
| RDSE2.REDIS_SHARD        | rdse2.redis_server_        | Shard-level Redis server metrics                   |
| RDSE2.REDIS_NODE         | rdse2.node_                | Node-level metrics including x509 certificates     |
| RDSE2.REDIS_INFO         | rdse2.node_                | Node information metrics                            |
| REDIS2.REPLICATION       | rdse2.database_syncer_     | Database replication metrics                        |
| REDIS2.SHARDREPL         | rdse2.redis_crdt_          | Shard-level CRDT replication metrics               |
| REDIS2.LDAP              | rdse2.directory_           | LDAP directory service metrics                     |
| REDIS2.NETWORK           | rdse2.node_network_        | Network interface metrics                           |
| REDIS2.MEMORY            | rdse2.node_memory_         | Memory usage metrics                                |
| REDIS2.X509              | rdse2.x509_                | X509 certificate metrics                            |
| REDIS2.DISK              | rdse2.node_disk_           | Disk I/O metrics                                    |
| REDIS2.FILESYSTEM        | rdse2.node_filesystem_     | Filesystem usage metrics                            |
| REDIS2.PROCESS           | rdse2.node_processes_      | Process metrics                                     |
| REDIS2.PRESSURE          | rdse2.node_pressure_       | System pressure metrics                             |
| REDIS2.FLASH             | rdse2.node_*_flash         | Flash storage metrics                               |
| REDIS2.SEARCH            | rdse2.redis_server_search_ | RediSearch module metrics                           |

### Validation

1. Ensure you can ping the host, particularly in a cloud environment. Run `wget --no-check-certificate <endpoint>` 
or `curl -k <endpoint>` to ensure that you can receive metrics.

2. Check the [status][5] of the Datadog agent.


## Data Collected

This release collects comprehensive metrics for clusters, databases, nodes, and shards. Default metric groups include RDSE2.REDIS_CLUSTER, RDSE2.REDIS_DATABASE, RDSE2.REDIS_SHARD, RDSE2.REDIS_NODE, and RDSE2.REDIS_INFO.

Use the `extra_metrics` parameter to collect additional data for replication, LDAP, network, memory, X509 certificates, disk, filesystem, processes, pressure, flash storage, and search. See the complete list in the [configuration](#configuration) section.


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
[4]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise_prometheus/datadog_checks/redis_enterprise_prometheus/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise_prometheus/metadata.csv
[7]: mailto:field.engineers@redis.com
[8]: https://redis.io/support/
[9]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=containerized
[10]: https://redis.io/docs/latest/integrate/prometheus-with-redis-enterprise/prometheus-metrics-definitions/
[11]: https://docs.datadoghq.com/integrations/redis-enterprise/
