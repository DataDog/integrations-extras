# Agent Check: Aqua

## Overview

This check monitors [Aqua][1].

## Setup

### Installation

The Aqua check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `aqua.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your Aqua performance data.
   See the [sample aqua.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4]

### Validation

[Run the Agent's `status` subcommand][5] and look for `aqua` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Service Checks

**aqua.can_connect**:

Returns CRITICAL if the Agent cannot connect to Aqua to collect metrics. Returns OK otherwise.

### Events

Aqua does not include any events.

## Troubleshooting

Need help? Contact [Datadog Support][7].

[1]: https://www.aquasec.com
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://github.com/DataDog/integrations-core/blob/master/aqua/datadog_checks/aqua/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[5]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/aqua/metadata.csv
[7]: https://docs.datadoghq.com/help/
