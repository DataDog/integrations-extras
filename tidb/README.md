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

> Current TiDB integration version: `1.0.0`

#### Host

Run `datadog-agent integration install -t datadog-tidb==<INTEGRATION_VERSION>`.

#### Containerized

The best way to use this integration with the Docker Agent is to build the Agent with this integration installed. Use the following Dockerfile to build an updated version of the Agent:

```dockerfile
FROM gcr.io/datadoghq/agent:latest

ARG INTEGRATION_VERSION=1.0.0

RUN agent integration install -r -t datadog-tidb==${INTEGRATION_VERSION}
```

Build the image and push it to your private Docker registry.

Then, upgrade the Datadog Agent container image. If the Helm chart is used, modify the `agents.image` section in the `values.yaml` to replace the default agent image:

```yaml
agents:
  enabled: true
  image:
    tag: <NEW_TAG>
    repository: <YOUR_PRIVATE_REPOSITORY>/<AGENT_NAME>
```

Use the new `values.yaml` to upgrade the Agent:

```shell
helm upgrade -f values.yaml <RELEASE_NAME> datadog/datadog
```

### Configuration

#### Host

##### Metric collection

1. Edit the `tidb.d/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your TiDB performance data. See the [sample tidb.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

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

#### Containerized

##### Metric collection

For containerized environments, after the TiDB check is integrated in the Datadog Agent image, Autodiscovery is configured by default.

Thus, metrics are automatically collected to Datadog's server.

If you need to override the default Autodiscovery behavior, add Datadog annotations to TiDB Pods:

```yaml
apiVersion: v1
kind: Pod
# (...)
metadata:
  name: '<POD_NAME>'
  annotations:
    ad.datadoghq.com/tidb.check_names: '["tidb"]'
    ad.datadoghq.com/tidb.init_configs: '[{}]'
    ad.datadoghq.com/tidb.instances: '[{"pd_metric_url": "http://%%host%%:2379/metrics", "tidb_metric_url": "http://%%host%%:10080/metrics", "tikv_metric_url": "http://%%host%%:20180/metrics"}]'
    # (...)
spec:
  containers:
    - name: 'tidb'
# (...)
```

See the [Autodiscovery Integration Templates][2] for the complete guidance.

##### Log collection

_Available for Agent versions >6.0_

Collecting logs is disabled by default in the Datadog Agent. To enable it, see [Kubernetes log collection documentation][9].

| Parameter      | Value                                                  |
| -------------- | ------------------------------------------------------ |
| `<LOG_CONFIG>` | `{"source": "tidb", "service": "tidb_cluster"}` |

### Validation

[Run the Agent's status subcommand][5] and look for `tidb` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

Service Checks are based on `tidb_cluster.prometheus.health` metrics. This check is controlled by the `health_service_check` config and default to `true`.
You can modify is in config `tidb.yml` file.

### Events

TiDB check does not include any events.

## Troubleshooting

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
