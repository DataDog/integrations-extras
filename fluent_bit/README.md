# Agent Check: Fluent Bit

## Overview

This check monitors [Fluent Bit][1] through the Datadog Agent.

## Fluent Bit configuration
Fluent Bit doesn't expose its internal metrics by default. You need to enable the built-in HTTP server that exposes the metrics endpoint.
```
[SERVICE]
    http_server on
```
Please see the official [documentation][2] for more information.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

To install the Fluent Bit check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build fluent_bit` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/fluent_bit/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `fluent_bit.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your fluent_bit performance data.
    ```yaml
    init_config:

    instances:
        ## @param metrics_endpoint - string - required
        ## The URL to Fluent Bit internal metrics per loaded plugin in Prometheus format.
        #
      - metrics_endpoint: http://127.0.0.1:2020/api/v1/metrics/prometheus
    ```
   See the [sample fluent_bit.d/conf.yaml][4] for all available configuration options.

3. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `fluent_bit` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The Fluent Bit integration does not include any events.

### Service Checks

The Fluent Bit integration does not include any service checks.

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://fluentbit.io
[2]: https://docs.fluentbit.io/manual/administration/monitoring
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[5]: https://github.com/DataDog/integrations-core/blob/master/check/datadog_checks/check/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-core/blob/master/check/metadata.csv
[9]: https://github.com/DataDog/integrations-core/blob/master/check/assets/service_checks.json
[10]: https://docs.datadoghq.com/help/
