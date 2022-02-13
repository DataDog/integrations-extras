# NS1 Integration

## Overview

This integration monitors [NS1][1] services through the Datadog Agent

![Snap](https://raw.githubusercontent.com/DataDog/integrations-extras/master/ns1/images/overview.png)

## Setup

The NS1 check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the NS1 check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-ns1==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `ns1.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting NS1 metrics. See the sample [ns1.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

Run the [Agent's status subcommand][4] and look for `ns1` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The NS1 integration does not include any events.

### Service Checks

See [service_checks.json][10] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][8].

## Further Reading

Additional helpful documentation, links, and articles:

- [NS1 + Datadog Integration (Outbound) Quick Start Guide][9]
- [Monitor NS1 with Datadog][11]


[1]: https://ns1.com/
[2]: https://app.datadoghq.com/account/settings#agent/overview
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentabovev68
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/ns1/datadog_checks/ns1/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/ns1/metadata.csv
[8]: https://docs.datadoghq.com/help/
[9]: https://help.ns1.com/hc/en-us/articles/4402752547219
[10]: https://github.com/DataDog/integrations-extras/blob/master/ns1/assets/service_checks.json
[11]: https://www.datadoghq.com/blog/ns1-monitoring-datadog/
