# Agent Check: Resilience4j

## Overview

[Resilience4j](https://github.com/resilience4j/resilience4j) is a lightweight fault tolerance library inspired by Netflix Hystrix, but designed for functional programming. This check monitors [Resilience4j][1] through the Datadog Agent.

## Setup

### Installation

To install the Resilience4j check on your host:

1. Install the [developer toolkit]
(<https://docs.datadoghq.com/developers/integrations/python/>)
 on any machine.

2. Run `ddev release build resilience4j` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/resilience4j/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `resilience4j/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Resilience4j performance data. See the [sample resilience4j/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `resilience4j` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Service Checks

The Resilience4j integration does not include any service checks.

### Events

Resilience4j does not include any events.

## Troubleshooting

Need help? Contact the [maintainer][8] of this integration.

[1]: https://resilience4j.readme.io/docs/micrometer#prometheus
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/resilience4j/datadog_checks/resilience4j/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/resilience4j/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/resilience4j/manifest.json
