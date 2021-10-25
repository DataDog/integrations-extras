# Agent Check: TiDB

## Overview

Connect [TiDB][1] cluster to Datadog in order to:

- Collect key TiDB metrics of your cluster.
- Collect logs of your cluster, such as TiDB/TiKV/TiFlash logs and slow query logs.
- Visualize cluster performance on the provided dashboard.

> **Note:** 
>
> - TiDB 4.0+ is required for this integration. 
> - Integration of TiDB Cloud with Datadog is not available now.

## Setup

### Installation

First, [download and launch the Datadog Agent][8].

Then, manually install the TiDB check. [Instructions vary depending on the environment][10]. 

#### Host

Run `datadog-agent integration install -t datadog-tidb==<INTEGRATION_VERSION>`.

### Configuration

##### Metric collection

1. Edit the `tidb.d/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your TiDB performance data. See the [sample tidb.d/conf.yaml][3] for all available configuration options.
   
  The [sample tidb.d/conf.yaml][3] only configures the PD instance. You need to manually configure the other instances in the TiDB cluster. Like this:

  ```yaml
  init_config:
  
  instances:
  
    - pd_metric_url: http://localhost:2379/metrics
      max_returned_metrics: 10000
      send_distribution_buckets: true
      tags:
        - tidb_cluster_name:cluster01
  
    - tidb_metric_url: http://localhost:10080/metrics
      max_returned_metrics: 10000
      send_distribution_buckets: true
      tags:
        - tidb_cluster_name:cluster01
  
    - tikv_metric_url: http://localhost:20180/metrics
      max_returned_metrics: 10000
      send_distribution_buckets: true
      tags:
        - tidb_cluster_name:cluster01
  
    - tiflash_metric_url: http://localhost:8234/metrics
      max_returned_metrics: 10000
      send_distribution_buckets: true
      tags:
        - tidb_cluster_name:cluster01
  
    - tiflash_proxy_metric_url: http://localhost:20292/metrics
      max_returned_metrics: 10000
      send_distribution_buckets: true
      tags:
        - tidb_cluster_name:cluster01
  ```

3. [Restart the Agent][4].

##### Log collection

_Available for Agent versions >6.0_

1. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

   ```yaml
   logs_enabled: true
   ```

2. Add this configuration block to your `tidb.d/conf.yaml` file to start collecting your TiDB logs:

   ```yaml
   logs:
    # pd log
    - type: file
      path: "/tidb-deploy/pd-2379/log/pd*.log"
      service: "tidb-cluster"
      source: "pd"
   
    # tikv log
    - type: file
      path: "/tidb-deploy/tikv-20160/log/tikv*.log"
      service: "tidb-cluster"
      source: "tikv"
   
    # tidb log
    - type: file
      path: "/tidb-deploy/tidb-4000/log/tidb*.log"
      service: "tidb-cluster"
      source: "tidb"
      exclude_paths:
        - /tidb-deploy/tidb-4000/log/tidb_slow_query.log
    - type: file
      path: "/tidb-deploy/tidb-4000/log/tidb_slow_query*.log"
      service: "tidb-cluster"
      source: "tidb"
      log_processing_rules:
        - type: multi_line
          name: new_log_start_with_datetime
          pattern: '#\sTime:'
      tags:
        - "custom_format:tidb_slow_query"
   
    # tiflash log
    - type: file
      path: "/tidb-deploy/tiflash-9000/log/tiflash*.log"
      service: "tidb-cluster"
      source: "tiflash"
   ```

   Change the `path` and `service` according to your cluster's configuration. 
   
   Use these commands to show all log path:
   
   ```shell
   # show deploying directories
   tiup cluster display <YOUR_CLUSTER_NAME>
   # find specific logging file path by command arguments
   ps -fwwp <TIDB_PROCESS_PID/PD_PROCESS_PID/etc.>
   ```

3. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `tidb` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Events

TiDB check does not include any events.

### Service Checks

Service Checks are based on `tidb_cluster.prometheus.health` metrics. This check is controlled by the `health_service_check` config and default to `true`.
You can modify this behavior in `tidb.yml` file.

See [service_checks.json][11] for a list of service checks provided by this integration.

## Troubleshooting

### Too many metrics

The TiDB check enables Datadog's `distribution` metric type by default. This part of data is quite large and may consume lots of resources. You can modify this behavior in `tidb.yml` file:

- `send_distribution_buckets: false`

Since there are many important metrics in a TiDB cluster, the TiDB check sets `max_returned_metrics` to `10000` by default. You can decrease `max_returned_metrics` in `tidb.yml` file if necessary:

- `max_returned_metrics: 1000`

Need help? Contact [Datadog support][7].

[1]: https://docs.pingcap.com/tidb/stable
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/tidb/datadog_checks/tidb/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/tidb/metadata.csv
[7]: https://docs.datadoghq.com/help/
[8]: https://app.datadoghq.com/account/settings#agent
[9]: https://docs.datadoghq.com/agent/kubernetes/log/
[10]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[11]: https://github.com/DataDog/integrations-extras/blob/master/tidb/assets/service_checks.json
