# Agent Check: Redpanda

## Overview

This Datadog-[Redpanda][1] integration collects key metrics from Redpanda by default. It can also be configured to add additional metric groups based on specific user needs.

Redpanda is a Kafka API compatible streaming platform for mission-critical workloads.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the redpanda check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build redpanda` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/redpanda/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `redpanda.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your redpanda performance data. See the [sample redpanda.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `redpanda` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Events

The redpanda integration does not include any events.

### Service Checks

The redpanda integration does not include any service checks.

See [service_checks.json][7] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][8].


[1]: https://vectorized.io
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/redpanda/datadog_checks/redpanda/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/redpanda/metadata.csv
[7]: https://github.com/DataDog/integrations-extras/blob/master/redpanda/assets/service_checks.json
[8]: https://docs.datadoghq.com/help/
