# Agent Check: Argo_CD

## Overview

This check monitors [Argo_CD][1] through the Datadog Agent.

## Setup

The Argo_CD check is not included in the Datadog Agent package, so you need to install it.
### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Argo_CD check on your host. See Use Community Integrations to install with the Docker Agent or earlier versions of the Agent.


1. Run the following command to install the Agent integration:

```
datadog-agent integration install -t datadog-cyral==<INTEGRATION_VERSION>
```

2. Configure your integration similar to core integrations.


### Configuration

1. Edit the `argo_cd.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your argo_cd performance data. See the [sample argo_cd.d/conf.yaml][3] for all available configuration options.

```bash
init_config:

instances:
 # url of the metrics endpoint of prometheus
 - prometheus_url: http://localhost:8082/metrics
```

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `argo_cd` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Events

The Argo_CD integration does not include any events.

### Service Checks

The Argo_CD integration does not include any service checks.

See [service_checks.json][7] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][8].


[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/argo_cd/datadog_checks/argo_cd/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/argo_cd/metadata.csv
[7]: https://github.com/DataDog/integrations-core/blob/master/argo_cd/assets/service_checks.json
[8]: https://docs.datadoghq.com/help/
