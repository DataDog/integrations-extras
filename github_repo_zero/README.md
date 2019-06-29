# Agent Check: Github_repo_zero

## Overview

This check monitors [Github_repo_zero][1] through the Datadog Agent.

## Setup

### Installation

The Github_repo_zero check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `github_repo_zero.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your github_repo_zero performance data. See the [sample github_repo_zero.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `github_repo_zero` under the Checks section.

## Data Collected

### Metrics

Github_repo_zero does not include any metrics.

### Service Checks

Github_repo_zero does not include any service checks.

### Events

Github_repo_zero does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].


[1]: **LINK_TO_INTEGERATION_SITE**
[2]: https://github.com/DataDog/integrations-core/blob/master/github_repo_zero/datadog_checks/github_repo_zero/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help
