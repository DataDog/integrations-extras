# Agent Check: ScaleOps

## Overview

[ScaleOps][13] is an autonomous Kubernetes resource management and cost optimization platform. It continuously rightsizes pods, manages HPA configurations, and consolidates workloads based on actual behavior, eliminating manual resource configuration.

This integration scrapes the Prometheus metrics exposed by the ScaleOps agent (`scaleops_*`) and provides visibility into automation score, workload recommendations, resource allocation, evictions, and estimated costs. It lets you replace ad-hoc `scaleops_*` custom metrics with an official, curated integration.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the ScaleOps check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-scaleops==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

1. Edit the `scaleops.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your ScaleOps metrics. See the [sample scaleops.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `scaleops` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The ScaleOps integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/scaleops/datadog_checks/scaleops/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/scaleops/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/scaleops/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://docs.scaleops.com
