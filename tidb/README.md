# Agent Check: TiDB

## Overview

TiDB check monitors the overall health and performance of a [TiDB][1] cluster.

## Setup

### Installation

Since TiDB check has not been added to [Datadog Agent][8] yet, users need to manually install TiDB check.

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build tidb` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/tidb/dist/<ARTIFACT_NAME>.whl`.

### Configuration

#### Host

##### Metric Collection

1. Edit the `tidb.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your tidb performance data. See the [sample tidb.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

##### Log Collection

_Available for Agent versions >6.0_

1. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

   ```yaml
   logs_enabled: true
   ```

2. Add this configuration block to your `tidb.d/conf.yaml` file to start collecting your tidb logs:

   ```yaml
     logs:
      # pd log
      - type: file
        path: "/tidb-deploy/pd-2379/log/pd*.log"
        service: "tidb-cluster"
        source: "pd"
        log_processing_rules:
          - type: multi_line
            name: new_log_start_with_datetime
            pattern: \[\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\s\+\d{2}:\d{2}\]
     
      # tikv log
      - type: file
        path: "/tidb-deploy/tikv-20160/log/tikv*.log"
        service: "tidb-cluster"
        source: "tikv"
        log_processing_rules:
          - type: multi_line
            name: new_log_start_with_datetime
            pattern: \[\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\s\+\d{2}:\d{2}\]
     
      # tidb log
      - type: file
        path: "/tidb-deploy/tidb-4000/log/tidb*.log"
        service: "tidb-cluster"
        source: "tidb"
        log_processing_rules:
          - type: multi_line
            name: new_log_start_with_datetime
            pattern: \[\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\s\+\d{2}:\d{2}\]
        exclude_paths:
          - /tidb-deploy/tidb-4000/log/tidb_slow_query.log
      - type: file
        path: "/tidb-deploy/tidb-4000/log/tidb_slow_query.log"
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
        log_processing_rules:
          - type: multi_line
            name: new_log_start_with_datetime
            pattern: \[\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\s\+\d{2}:\d{2}\]
        exclude_paths:
          - /tidb-deploy/tiflash-9000/log/tiflash_cluster_manager.log
          - /tidb-deploy/tiflash-9000/log/tiflash_error.log
      - type: file
        path: "/tidb-deploy/tiflash-9000/log/tiflash_cluster_manager.log"
        service: "tidb-cluster"
        source: "tiflash"
        log_processing_rules:
          - type: multi_line
            name: new_log_start_with_datetime
            pattern: \d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\,\d{3}
        tags:
          - "custom_format:tiflash_cluster_manager"
      - type: file
        path: "/tidb-deploy/tiflash-9000/log/tiflash_error.log"
        service: "tidb-cluster"
        source: "tiflash"
        log_processing_rules:
          - type: multi_line
            name: new_log_start_with_datetime
            pattern: \[\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\s\+\d{2}:\d{2}\]
   ```

   Change the `path` and `service` parameter values and configure them for your environment. See the [sample tidb.d/conf.yaml][3] for all available configuration options.

   To make sure that stacktraces are properly aggregated as one single log, a [multiline processing rule][7] can be added.


#### Containerized

##### Metric collection

For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying the parameters below.

| Parameter            | Value                                                    |
| -------------------- | -------------------------------------------------------- |
| `<INTEGRATION_NAME>` | `tidb`                                                   |
| `<INIT_CONFIG>`      | blank or `{}`                                            |
| `<INSTANCE_CONFIG>`  | `{"prometheus_url":"http://%%host%%:8080/_status/vars"}` |
| `<LOG_CONFIG>     `  | blank or `{}`                                            |

##### Log collection

_Available for Agent versions >6.0_

Collecting logs is disabled by default in the Datadog Agent. To enable it, see [Kubernetes log collection documentation][10].

| Parameter      | Value                                                  |
| -------------- | ------------------------------------------------------ |
| `<LOG_CONFIG>` | `{"source": "cassandra", "service": "<SERVICE_NAME>"}` |

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Validation

[Run the Agent's status subcommand][5] and look for `tidb` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

TiDB check does not include any service checks.

### Events

TiDB check does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://docs.pingcap.com/tidb/stable
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/tidb/datadog_checks/tidb/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/tidb/metadata.csv
[7]: https://docs.datadoghq.com/help/
[8]: https://app.datadoghq.com/account/settings#agent