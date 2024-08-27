# Agent Check: Redis Enterprise

## Overview

Redis is a fast, versatile data store that supports a variety of data structures, including strings, hashes, lists, sets, streams, and more. It also offers programmability, extensibility, persistence, clustering, and high availability. The community edition of Redis adds additional data models and capabilities, which include vector search, probabilistic data structures, JSON support, and full-text search.

This integration works with on-premises and private cloud installations of [Redis Enterprise][1].
The integration provides metrics for three critical cluster components: databases, nodes, and shards. This allows you to monitor database throughput, memory utilization, CPU usage, connection counts, replication health, and a variety of additional metrics within Datadog.
You can use this information to understand the overall health of your Redis Enterprise clusters, diagnose application performance issues, and prevent downtime.

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

Set the `openmetrics_endpoint` to point to your cluster. See the [example][4]. Leave `tls_verify` set to false.

There are two optional parameters: extra_metrics, and excluded_metrics, as noted in the example configuration file. 

The extra_metrics parameter takes a list of metric groups. The following are the available groups: RDSE.REPLICATION, RDSE.LISTENER, RDSE.PROXY, RDSE.BIGSTORE, RDSE.FLASH, 
RDSE.SHARDREPL. The default metric groups are RDSE.NODE, RDSE.DATABASE, and RDSE.SHARD. They are automatically inserted by the integration.

The exclude_metrics parameter takes a list of individual metrics to exclude, meaning that this information will not be 
passed on to Datadog. The individual metrics should be stripped of their prefix, eg. 'rdse.bdb_up' would become 'bdb_up'. 
The full list of metrics is available on the 'Data Collected' tab of the integration page. For reference the following 
groups use the associated prefixes; they can be used to search for individual metrics on the data collected page. 

| Group             | Prefix                      |
|-------------------|-----------------------------|
| Node¹             | rdse.node_                  |
| Database²         | rdse.bdb_                   |
| Shard³            | rdse.redis_                 |
| Replication       | rdse.bdb_crdt_              |
 | Replication       | rdse.bdb_replicaof_         |
 | Shard Replication | rdse.redis_crdt_            |
 | Proxy             | rdse.dmcproxy_              |
 | Listener          | rdse.listener_              |
 | Bigstore          | rdse.node_bigstore_         |
 | Flash⁴            | rdse.node_available_flash   |

1: this will return bigstore metrics as well<br>
2: this will return replication metrics as well<br>
3: this will return shard replication metrics as well<br>
4: all flash metrics are of the form: rdse.node_*_flash

### Validation

1. Ensure you can ping the machine, particularly in a cloud environment. Run `wget --no-check-certificate <endpoint>` 
or `curl -k <endpoint>` to ensure that you can receive metrics.

2. Check the [status][5] of the Datadog agent.


## Data Collected

The current release gathers all metrics for databases, nodes, and shards. Optionally, via the extra_metrics parameter, 
data for replication, proxy, listener, etc. can be gathered (see the list in the Configuration section).


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
