# Agent Check: Aws_pricing

## Overview

This check monitors [Aws_pricing][1] through the Datadog Agent.

## Setup

### Installation

The Aws_pricing check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `aws_pricing.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your aws_pricing performance data. See the [sample aws_pricing.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `aws_pricing` under the Checks section.

## Data Collected

### Metrics

Aws_pricing does not include any metrics.

### Service Checks

Aws_pricing does not include any service checks.

### Events

Aws_pricing does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: **LINK_TO_INTEGERATION_SITE**
[2]: https://github.com/DataDog/integrations-core/blob/master/aws_pricing/datadog_checks/aws_pricing/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help
