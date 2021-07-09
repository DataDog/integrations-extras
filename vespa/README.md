# Vespa Integration

## Overview

Gather metrics from your [Vespa][1] system in real time to:

- Visualize and monitor Vespa state and performance
- Alert on health and availability

## Setup

The Vespa check is not included in the [Datadog Agent][2] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Vespa check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior to version 6.8][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][2].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-vespa==<INTEGRATION_VERSION>
   ```
3. Configure your integration like [any other packaged integration][6].

### Configuration

To configure the Vespa check:

1. Create a `vespa.d/` folder in the `conf.d/` folder at the root of your [Agent's configuration directory][8].
2. Create a `conf.yaml` file in the `vespa.d/` folder previously created.
3. See the [sample vespa.d/conf.yaml][10] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to configure the `consumer`, which decides the set of metrics forwarded by the check:
   - `consumer`: The consumer to collect metrics for, either `default` or a [custom consumer][9]
     from your Vespa application's services.xml.
5. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `vespa` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

**vespa.metrics_health**:<br>
Returns `CRITICAL` if there is no response from the Vespa [Node metrics API][11]. Returns `WARNING` if there is a
response from the Vespa [Node metrics API][11] but there was an error in processing, otherwise returns `OK`.

**vespa.process_health**:<br>
For each Vespa process, returns `CRITICAL` if the process seems to be down (the Vespa [Node metrics API][11] fails to connect to the process).
Returns `WARNING` if the process status is unknown (the Vespa [Node metrics API][11] can connect to the process, but
gets an error in the response), otherwise returns `OK`.

### Events

The Vespa integration does not include any events.

### Service Checks

See [service_checks.json][12] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][5].


[1]: https://vespa.ai/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help/
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/vespa/metadata.csv
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://docs.vespa.ai/documentation/reference/services-admin.html#metrics
[10]: https://github.com/DataDog/integrations-extras/blob/master/vespa/datadog_checks/vespa/data/conf.yaml.example
[11]: https://docs.vespa.ai/documentation/reference/metrics.html#node-metrics-api
[12]: https://github.com/DataDog/integrations-extras/blob/master/vespa/assets/service_checks.json
