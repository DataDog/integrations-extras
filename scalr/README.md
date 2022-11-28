# Scalr Integration

## Overview

Scalr Datadog [integration][18] streams Terraform run execution [event][19] details as well as metrics, like runs queue and workspace count, to Datadog for in depth analysis and reporting.
Metrics include information about number of environments, workspaces, runs, and state of the queue, and many others.

## Setup
The Scalr integration is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For the Datadog Agent v7.21 or v6.21 and later, follow these instructions to install the Scalr integration on your host. See [Use Community Integrations][3] to install it with the Docker Agent or earlier versions of the Datadog Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-scalr==1.0.0
   ```

2. Configure your integration similar to an Agent-based [integration][4].

### Configuration

1. Edit the `scalr.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your [Scalr metrics](#metrics). See the [sample scalr.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

Run the [Agent's status subcommand][10] and look for `scalr` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

### Events

Scalr sends run execution results as an event to the [Events Explorer][17].

## Troubleshooting

Need help? Contact [Datadog support][5] or [Scalr support][15].

## Further Reading

- [Scalr customer documentation][16]
- [Scalr Datadog integration documentation][14]

[1]: https://scalr.io
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://docs.datadoghq.com/help/
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/scalr/datadog_checks/scalr/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/scalr/metadata.csv
[13]: https://github.com/DataDog/integrations-extras/blob/master/scalr/assets/service_checks.json
[14]: https://docs.scalr.com/en/latest/integrations.html#datadog
[15]: https://scalr-labs.atlassian.net/servicedesk/customer/portal/31
[16]: https://docs.scalr.com
[17]: https://docs.datadoghq.com/events/explorer/
[18]: https://docs.scalr.com/en/latest/integrations.html
[19]: https://docs.datadoghq.com/events/

