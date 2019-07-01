# Agent Check: github_repo_two

## Overview

This check monitors [github_repo_two][1] through the Datadog Agent.

## Setup

### Installation

The github_repo_two check is not included in the [Datadog Agent][2] package, so it must
be installed manually.

### Configuration

1. Edit the `github_repo_two.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your github_repo_two performance data. See the [sample github_repo_two.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `github_repo_two` under the Checks section.

## Data Collected

### Metrics

github_repo_two does not include any metrics.

### Service Checks

github_repo_two does not include any service checks.

### Events

github_repo_two does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://github.com/DataDog/integrations-core/blob/master/github_repo_two/datadog_checks/github_repo_two/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[5]: https://docs.datadoghq.com/help
