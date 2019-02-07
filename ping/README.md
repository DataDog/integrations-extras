# Agent Check: Ping

## Overview

This check monitors [Ping][1].

## Setup

### Installation

The Ping check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `ping.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your ping performance data.
   See the [sample ping.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3]

### Validation

[Run the Agent's `status` subcommand][4] and look for `ping` under the Checks section.

## Data Collected

### Metrics

Ping does not include any metrics.

### Service Checks

Ping does not include any service checks.

### Events

Ping does not include any events.

## Troubleshooting

Need help? Contact [Datadog Support][5].

[1]: **LINK_TO_INTEGERATION_SITE**
[2]: https://github.com/DataDog/integrations-core/blob/master/ping/datadog_checks/ping/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help/
