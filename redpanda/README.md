# Agent Check: Redpanda

## Overview

This Datadog-[Redpanda][1] integration collects key metrics from Redpanda by default. It can also be configured to add additional metric groups based on specific user needs.

Redpanda is a Kafka API compatible streaming platform for mission-critical workloads.

## Setup

### Installation

First, [download and launch the Datadog Agent][9].

Then, manually install the Redpanda check. [Instructions vary depending on the environment][10].

> Current Redpanda integration version: `1.0.0`

#### Host

Run `datadog-agent integration install -t datadog-redpanda==<INTEGRATION_VERSION>`.

#### Containerized

The best way to use this integration with the Docker Agent is to build the Agent with this integration installed. Use the following Dockerfile to build an updated version of the Agent:

```dockerfile
FROM gcr.io/datadoghq/agent:latest

ARG INTEGRATION_VERSION=1.0.0

RUN agent integration install -r -t datadog-redpanda==${INTEGRATION_VERSION}
```

Build the image and push it to your private Docker registry.

Then, upgrade the Datadog Agent container image. If the Helm chart is used, modify the `agents.image` section in the `values.yaml` to replace the default agent image:

```yaml
agents:
  enabled: true
  image:
    tag: <NEW_TAG>
    repository: <YOUR_PRIVATE_REPOSITORY>/<AGENT_NAME>
```

Use the new `values.yaml` to upgrade the Agent:

```shell
helm upgrade -f values.yaml <RELEASE_NAME> datadog/datadog
```

### Configuration

#### Host

##### Metric collection

1. Edit the `redpanda.d/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Redpanda performance data. See the sample [redpanda.d/conf.yaml.example][3] for all available configuration options.

2. [Restart the Agent][4].

##### Log collection

_Available for Agent versions >6.0_

1. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

   ```yaml
   logs_enabled: true
   ```

2. Add this configuration block to your `redpanda.d/conf.yaml` file to start collecting your Redpanda logs:

   ```yaml
    logs:
    - type: journald
      source: redpanda
    ```

#### Containerized

##### Metric collection

For containerized environments, after the Redpanda check is integrated in the Datadog Agent image, Autodiscovery is configured by default.

Thus, metrics are automatically collected to Datadog's server.

See the [Autodiscovery Integration Templates][2] for the complete guidance.

##### Log collection

_Available for Agent versions >6.0_

Collecting logs is disabled by default in the Datadog Agent. To enable it, see [Kubernetes log collection documentation][9].

| Parameter      | Value                                                  |
| -------------- | ------------------------------------------------------ |
| `<LOG_CONFIG>` | `{"source": "redpanda", "service": "redpanda_cluster"}` |

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
[9]: https://app.datadoghq.com/account/settings#agent
[10]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
