# Agent Check: Grafana

## Overview

Grafana is a multi-platform open source analytics and interactive visualization web application. This check monitors [Grafana][1] through the Datadog Agent.

## Setup

### Installation

To install the Grafana check on your host:

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/python/)
 on any machine.

2. Run `ddev release build grafana` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/grafana/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Enable the internal Grafana metrics using the [Grafana config file](https://github.com/grafana/grafana/blob/c98259f74a835429ed2db6cca2c64a3802ebc43f/conf/defaults.ini#L1747)

    ```
    #################################### Internal Grafana Metrics ############
    # Metrics available at HTTP URL /metrics and /metrics/plugins/:pluginId
    [metrics]
    enabled = true
    ```

2. Edit the `grafana/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Grafana metrics. See the [sample grafana/conf.yaml][4] for all available configuration options.

3. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `grafana` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The Grafana integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://grafana.com/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/containers/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/grafana/datadog_checks/grafana/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/configuration/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/configuration/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/grafana/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/grafana/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
