# Vespa Integration

## Overview

Gather metrics from your [Vespa][1] system in real time to:

- Visualize and monitor Vespa state and performance
- Alert on health and availability

## Setup

The Vespa check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Vespa check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-vespa==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

To configure the Vespa check:

1. Create a `vespa.d/` folder in the `conf.d/` folder at the root of your [Agent's configuration directory][8].
2. Create a `conf.yaml` file in the `vespa.d/` folder previously created.
3. See the [sample vespa.d/conf.yaml][10] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to configure the `consumer`, which decides the set of metrics forwarded by the check:
   - `consumer`: The consumer to collect metrics for, either `default` or a [custom consumer][9]
     from your Vespa application's services.xml.
5. [Restart the Agent][5].

### Validation

Run the [Agent's status subcommand][6] and look for `vespa` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

The Vespa integration does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][13].


[1]: https://vespa.ai/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/vespa/metadata.csv
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://docs.vespa.ai/documentation/reference/services-admin.html#metrics
[10]: https://github.com/DataDog/integrations-extras/blob/master/vespa/datadog_checks/vespa/data/conf.yaml.example
[12]: https://github.com/DataDog/integrations-extras/blob/master/vespa/assets/service_checks.json
[13]: https://docs.datadoghq.com/help/
