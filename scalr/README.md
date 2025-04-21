# Scalr Integration

## Overview

Scalr is a terraform cloud alternative that provides you with the controls, visibility, and flexibility to decentralize your terraform operations in one place.

The Scalr [integration][15] sends Terraform run execution [event][16] details and metrics for in-depth analysis and reporting such as queue runs, queue state, the number of environments, and workspace count. These metrics are visualized in their out-of-the-box dashboard to help correlate deployments with other infrastructure changes and to track trends within your Terraform pipeline.

## Setup
The Scalr integration is not included in the [Datadog Agent][1] package, so you need to install it.

### Installation

For the Datadog Agent v7.21 or v6.21 and later, follow these instructions to install the Scalr integration on your host. See [Use Community Integrations][2] to install it with the Docker Agent or earlier versions of the Datadog Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-scalr==1.0.0
   ```

2. Configure your integration similar to an Agent-based [integration][3].

### Configuration

1. Edit the `scalr.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][5] to start collecting your [Scalr metrics](#metrics). See the [sample scalr.d/conf.yaml][6] for all available configuration options.

2. [Restart the Agent][7].

### Validation

Run the [Agent's status subcommand][8] and look for `scalr` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][10] for a list of service checks provided by this integration.

### Events

Scalr sends run execution results as an event to the [Events Explorer][14].

## Troubleshooting

Need help? Contact [Datadog support][4] or [Scalr support][12].

## Further Reading

- [Scalr customer documentation][13]
- [Scalr Datadog integration documentation][11]

[1]: /account/settings/agent/latest
[2]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[3]: https://docs.datadoghq.com/getting_started/integrations/
[4]: https://docs.datadoghq.com/help/
[5]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[6]: https://github.com/DataDog/integrations-extras/blob/master/scalr/datadog_checks/scalr/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[9]: https://github.com/DataDog/integrations-extras/blob/master/scalr/metadata.csv
[10]: https://github.com/DataDog/integrations-extras/blob/master/scalr/assets/service_checks.json
[11]: https://docs.scalr.com/en/latest/integrations.html#datadog
[12]: https://scalr-labs.atlassian.net/servicedesk/customer/portal/31
[13]: https://docs.scalr.com
[14]: https://docs.datadoghq.com/events/explorer/
[15]: https://docs.scalr.com/en/latest/integrations.html
[16]: https://docs.datadoghq.com/events/

