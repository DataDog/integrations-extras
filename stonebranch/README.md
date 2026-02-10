# Agent Check: Stonebranch

## Overview

Stonebranch Universal Automation Center (UAC) is an enterprise workload automation platform used to orchestrate, schedule, and monitor complex workflows across distributed systems, applications, and infrastructure.

The Stonebranch integration provides visibility into UAC by scraping metrics exposed by the Universal Controller Prometheus endpoint and surfacing them in Datadog. This enables operations, SRE, and platform teams to monitor automation health, execution activity, and system capacity from a single observability platform.

The integration automatically collects a curated set of core UC metrics and supports optional metric groups for deeper JVM, process, and license-level insights. Metrics are enriched with labels emitted by the UC, enabling Datadog users to build workflow-, agent-, and controller-centric views and dashboards.

The integration collects the following Datadog telemetry types:
- **Metrics**: Task executions, workflow outcomes, agent and OMS status, controller health, database pools, and license usage.

With this integration, teams can proactively detect automation failures, capacity constraints, and infrastructure issues impacting workload execution.


## Setup

The Stonebranch check is not included in the [Datadog Agent][1] package and must be installed separately.

### Installation

Install the Stonebranch integration using the Datadog Agent integration command.  

1. Run the following command to install the integration:
```shell
   datadog-agent integration install -t datadog-stonebranch==<VERSION>
```

### Configuration

1. Edit the `stonebranch.d/conf.yaml` file in the `conf.d/` directory of your Datadog Agent configuration.

   The Universal Controller exposes metrics via its Prometheus endpoint and the Agent must be able to authenticate to it.

   Minimal configuration example:
```yaml
   instances:
     - openmetrics_endpoint: https://stonebranch.controller/uc/resources/metrics

       auth_type: basic
       username: <USERNAME>
       password: <PASSWORD>

       metric_groups:
         - jvm
         - process

       tags:
         - env:prod
         - service:stonebranch
```

   * Default metrics are always collected.
   * Optional metric groups can be enabled using `metric_groups`.
   * Individual metrics can be excluded using `exclude_metric_names`.

   See the sample `stonebranch.d/conf.yaml.example` file for the full list of available configuration options and check the [Stonebranch documentation][2] for the complete list of available metrics.

2. Restart the Datadog Agent.


### Validation

Run the Agent status command and verify that `stonebranch` appears under the **Checks** section:
```shell
datadog-agent status
```


## Metric Groups (Opt-in)

The Stonebranch integration always collects a curated set of core Universal Automation Center (UAC) metrics by default. These metrics provide visibility into task execution, workflows, controller health, agents, OMS connectivity, and overall system status.

Additional metrics are organized into **opt-in metric groups**. These groups allow you to selectively enable deeper visibility without collecting unnecessary metrics by default.

Metric groups are enabled using the `metric_groups` option in the instance configuration.

### Available Metric Groups

The following metric groups are supported:

* **jvm**
  Collects JVM-level metrics for the Universal Controller, including thread counts and memory usage.

* **process**
  Collects operating system process metrics such as CPU usage, resident memory, and open file descriptors for controller processes.

* **license_details**
  Collects detailed license consumption metrics, including agent counts, cluster nodes, task definitions, and monthly execution usage.

### Enabling Metric Groups

To enable one or more metric groups, add the `metric_groups` option to your instance configuration:
```yaml
instances:
  - openmetrics_endpoint: https://stonebranch.controller/uc/resources/metrics

    auth_type: basic
    username: <USERNAME>
    password: <PASSWORD>

    metric_groups:
      - jvm
      - process
```

Metric groups are additive. When enabled, the metrics in the selected groups are collected in addition to the default Stonebranch metrics.

### Excluding Individual Metrics

If you want to exclude specific metrics after defaults and metric groups have been expanded, use the `exclude_metric_names` option:
```yaml
exclude_metric_names:
  - uc_build_info
```

This option removes metrics by exact Prometheus metric name and is applied after all default and group-based metrics have been selected.

### Notes

* Default Stonebranch metrics are always collected and cannot be disabled.
* Metric groups are optional and disabled unless explicitly configured.
* Advanced OpenMetrics filtering options (such as regex-based exclusions and label-based filtering) are available through standard OpenMetrics configuration options. See the sample configuration file for details.


## Data Collected

### Metrics

The integration collects a curated set of Stonebranch metrics by default, including task execution counts, workflow status, agent and OMS health, and controller-level statistics.

Optional metric groups provide additional coverage:

* JVM metrics
* Process-level resource metrics
* License consumption and capacity metrics

See `metadata.csv` for the complete list of metrics exposed by this integration.

## Support

TBD

[1]: https://github.com/DataDog/integrations-extras
[2]: https://stonebranchdocs.atlassian.net/wiki/spaces/UC79/pages/1614446871/Universal+Controller+-+Provided+Metrics