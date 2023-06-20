
## Overview

Redpanda is a Kafka API-compatible streaming platform for mission-critical workloads.

Connect Datadog with [Redpanda][1] to view key metrics and add additional metric groups based on specific user needs.

## Setup

### Installation

1. [Download and launch the Datadog Agent][9].
2. Manually install the Redpanda integration. See [Use Community Integrations][10] for more details based on the environment.

<!-- xxx tabs xxx -->
<!-- xxx tab "Host" xxx -->

#### Host

To configure this check for an Agent running on a host, run `datadog-agent integration install -t datadog-redpanda==<INTEGRATION_VERSION>`.

<!-- xxz tab xxx -->
<!-- xxx tab "Containerized" xxx -->

#### Containerized

For containerized environments, the best way to use this integration with the Docker Agent is to build the Agent with the Redpanda integration installed. 

To build an updated version of the Agent:

1. Use the following Dockerfile:

```dockerfile
FROM gcr.io/datadoghq/agent:latest

ARG INTEGRATION_VERSION=1.0.0

RUN agent integration install -r -t datadog-redpanda==${INTEGRATION_VERSION}
```

2. Build the image and push it to your private Docker registry.

3. Upgrade the Datadog Agent container image. If you are using a Helm chart, modify the `agents.image` section in the `values.yaml` file to replace the default agent image:

```yaml
agents:
  enabled: true
  image:
    tag: <NEW_TAG>
    repository: <YOUR_PRIVATE_REPOSITORY>/<AGENT_NAME>
```

4. Use the new `values.yaml` file to upgrade the Agent:

```shell
helm upgrade -f values.yaml <RELEASE_NAME> datadog/datadog
```

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Configuration

<!-- xxx tabs xxx -->
<!-- xxx tab "Host" xxx -->

#### Host

##### Metric collection

To start collecting your Redpanda performance data:

1. Edit the `redpanda.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][11]. See the sample [redpanda.d/conf.yaml.example][3] file for all available configuration options.

2. [Restart the Agent][4].

##### Log collection

By default, collecting logs is disabled in the Datadog Agent. Log collection is available for Agent v6.0+.

1. To enable logs, add the following in your `datadog.yaml` file:

   ```yaml
   logs_enabled: true
   ```

2. Make sure `dd-agent` user is member of `systemd-journal` group, if not, run following command as root:
   ```
   usermod -a -G systemd-journal dd-agent
   ```

3. Add the following in your `redpanda.d/conf.yaml` file to start collecting your Redpanda logs:

   ```yaml
    logs:
    - type: journald
      source: redpanda
    ```

<!-- xxz tab xxx -->
<!-- xxx tab "Containerized" xxx -->

#### Containerized

##### Metric collection

For containerized environments, Autodiscovery is configured by default after the Redpanda check integrates in the Datadog Agent image.

Metrics are automatically collected in Datadog's server. For more information, see [Autodiscovery Integration Templates][2].

##### Log collection

By default, log collection is disabled in the Datadog Agent. Log collection is available for Agent v6.0+.

To enable logs, see [Kubernetes Log Collection][9].

| Parameter      | Value                                                  |
| -------------- | ------------------------------------------------------ |
| `<LOG_CONFIG>` | `{"source": "redpanda", "service": "redpanda_cluster"}` |

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Validation

[Run the Agent's status subcommand][5] and look for `redpanda` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Events

The Redpanda integration does not include any events.

### Service Checks


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
[11]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
