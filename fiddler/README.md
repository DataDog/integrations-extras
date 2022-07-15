# Agent Check: Fiddler

## Overview

This check monitors AI model performance using [Fiddler][1] through the Datadog Agent.
Fiddler monitors model drift and model performance for AI models.


## Setup

The Fiddler check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Fiddler check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-fiddler==1.0.0
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `fiddler.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Fiddler performance data. See the [sample `fiddler.d/conf.yaml`][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `fiddler` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

### Events

The Fiddler integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][10].

[1]: https://fiddler.ai
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/cloudsmith/datadog_checks/cloudsmith/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/fiddler/metadata.csv
[9]: https://github.com/DataDog/integrations-extras/blob/master/fiddler/assets/service_checks.json
[10]: https://docs.datadoghq.com/help/

