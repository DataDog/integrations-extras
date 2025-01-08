# Agent Check: Fluent Bit (Agent)

## Overview

This check monitors [Fluent Bit][1] metrics through the Datadog Agent. To send logs to Datadog with Fluent Bit and to learn about the Datadog Fluent Bit output plugin, see the [Fluent Bit][11] documentation.

## Fluent Bit configuration
Fluent Bit doesn't expose its internal metrics by default. You need to enable the built-in HTTP server that exposes the metrics endpoint.
```
[SERVICE]
    http_server on
```
See the official [documentation][2] for more information.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][4] for guidance on applying these instructions.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Fluent Bit check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-fluentbit==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `fluentbit.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your fluentbit performance data.
    ```yaml
    init_config:

    instances:
        ## @param metrics_endpoint - string - required
        ## The URL to Fluent Bit internal metrics per loaded plugin in Prometheus format.
        #
      - metrics_endpoint: http://127.0.0.1:2020/api/v1/metrics/prometheus
    ```
   See the [sample fluentbit.d/conf.yaml][5] file for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `fluentbit` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Events

The Fluent Bit integration does not include any events.

### Service Checks

The Fluent Bit integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][10].

## Further Reading

Additional helpful documentation, links, and articles:

- [Send Fluent Bit Logs to Datadog][11]


[1]: https://fluentbit.io
[2]: https://docs.fluentbit.io/manual/administration/monitoring
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/fluentbit/datadog_checks/fluentbit/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/fluentbit/metadata.csv
[9]: https://github.com/DataDog/integrations-extras/blob/master/fluentbit/assets/service_checks.json
[10]: https://docs.datadoghq.com/help/
[11]: https://docs.datadoghq.com/logs/guide/fluentbit/
[12]: https://docs.datadoghq.com/developers/integrations/python/
