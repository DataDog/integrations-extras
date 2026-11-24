# Agent Check: Volcano

## Overview

[Volcano][13] is a Kubernetes batch scheduler for AI/ML training, big data, and HPC workloads. It adds gang scheduling, queues with fair sharing and capacity limits, and preemption on top of Kubernetes.

This integration scrapes the Prometheus metrics exposed by the Volcano scheduler and controller manager (`volcano_*`) and provides visibility into:

- Scheduling session, action, plugin, and per-task stage latency.
- End-to-end job scheduling latency and unschedulable jobs and tasks.
- Allocated, requested, deserved, and capacity resources for each queue.
- Pod groups by phase in each queue, and completed and failed Volcano jobs.
- Preemption attempts and victims.

## Setup

### Installation

If you are using Datadog Agent v6.8+, follow the instructions below to install the Volcano check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-volcano==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

Metrics are enabled by default in the Volcano Helm chart (`custom.scheduler_metrics_enable` and `custom.controller_metrics_enable`). The scheduler serves them on port `8080` and the controller manager on port `8081`, both at `/metrics`. Configure one instance for each component.

1. Edit the `volcano.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your Volcano metrics. See the [sample volcano.d/conf.yaml][7] for all available configuration options.

   ```yaml
   init_config:

   instances:
     - openmetrics_endpoint: http://volcano-scheduler-service.volcano-system:8080/metrics
     - openmetrics_endpoint: http://volcano-controllers-service.volcano-system:8081/metrics
   ```

   On Kubernetes, you can use [Autodiscovery annotations][14] on the scheduler and controller manager pods instead. For example, for the scheduler:

   ```yaml
   ad.datadoghq.com/volcano-scheduler.checks: |
     {
       "volcano": {
         "instances": [{"openmetrics_endpoint": "http://%%host%%:8080/metrics"}]
       }
     }
   ```

2. [Restart the Agent][8].

Some queue metrics depend on the scheduler plugins: `volcano.queue.weight` is reported by the `proportion` plugin, and `volcano.queue.capacity.*` and `volcano.queue.real_capacity.*` by the `capacity` plugin.

### Validation

[Run the Agent's status subcommand][9] and look for `volcano` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The Volcano integration does not include any events.

## Support

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: /account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/volcano/datadog_checks/volcano/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/volcano/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/volcano/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://volcano.sh/
[14]: https://docs.datadoghq.com/containers/kubernetes/integrations/
