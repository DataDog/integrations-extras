# Agent Check: Ocient

## Overview

[Ocient][1] Hyperscale Data Warehouse is a data analytics software solutions company that enables all-the-time, compute-intensive analysis of large, complex datasets while optimizing for performance, cost, and energy efficiency.

With industry-standard interfaces like SQL and JDBC, Ocient makes it easy for organizations to interact with data within its platform.
This integration enables your Ocient Hyperscale Data Warehouse to send metrics to Datadog, including metrics related to query performance, disk usage, database tables, and more.

## Setup

### Installation

1. Run the following command to install the Agent integration:

   ```shell
   agent integration install -t datadog-ocient==1.0.0
   ```
   
2. Configure the integration by setting `openmetrics_endpoint` to your cluster's master node. See [Getting Started with Integrations][4] for more information.
3. [Restart][5] the Agent.

### Configuration

To configure this check for an Agent running on a host:

1. Edit the `ocient.d/conf.yaml` file, in the `conf.d/` folder at the root of your [Agent's configuration directory][3]. For all available configuration options, see the [sample ocient.d/conf.yaml][4].

```yaml
instances:

- use_openmetrics: true  # Enables OpenMetrics V2

  ## @param openmetrics_endpoint - string - required
  ## The URL exposing metrics in the OpenMetrics format.
  #
  openmetrics_endpoint: http://localhost:<PORT>/metrics
```

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `ocient` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Service Checks

Ocient does not include any service checks.

### Events

Ocient does not include any events.

## Troubleshooting

Need help? Contact [Ocient support][8].

[1]: https://ocient.com/
[2]: /account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-extras/blob/master/ocient/datadog_checks/ocient/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/ocient/metadata.csv
[8]: https://service.ocient.com/support/home
