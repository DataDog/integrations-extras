# Agent Check: Patroni

## Overview

#This check monitors [Patroni][1].
This check collects key metrics from your Patroni-managed PostgreSQL clusters, including cluster state, replication status, and database health. It also monitors your cluster's Distributed Configuration Store (DCS) and provides insights into failover and synchronization activity.

## Setup

### Installation

If you are using Agent v7.21+ / v6.21+ follow the instructions below to install the RedisEnterprise check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior < v7.21 / v6.21][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][2].
2. Run the following command to install the integrations wheel with the Agent:

   ```bash
   datadog-agent integration install -t datadog-patroni==<INTEGRATION_VERSION>
   ```
  You can find the latest version on the [Datadog Integrations Release Page][12]

   **Note**: If necessary, prepend `sudo -u dd-agent` to the install command.
   
3. Configure your integration like [any other packaged integration][6].

### Configuration

Copy the [sample configuration][7] and update the required sections to collect data from your Patroni cluster

```yaml
instances:

  -  openmetrics_endpoint: "http://127.0.0.1:8008/metrics"

```

### Validation

Run the [Agent's status subcommand][6] and look for `patroni` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/patroni/metadata.csv) for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json](https://github.com/DataDog/integrations-extras/blob/master/patroni/assets/service_checks.json) for a list of service checks provided by this integration

### Events

Patroni check includes failover events to dect when a failover event has occured:

- Patroni Failover Detected

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/patroni/datadog_checks/patroni/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/patroni/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/patroni/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/

