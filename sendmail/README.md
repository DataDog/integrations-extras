# Agent Check: Sendmail

## Overview

This check monitors [Sendmail][1] through the Datadog Agent.

## Setup

### Installation

The Sendmail check is not included in the [Datadog Agent][2] package, so it must
be installed manually.

### Configuration

1. Edit the `sendmail.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your sendmail performance data. See the [sample sendmail.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `sendmail` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.

### Service Checks

Sendmail does not include any service checks.

### Events

Sendmail does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://www.proofpoint.com/us/open-source-email-solution
[2]: https://github.com/DataDog/integrations-extras/blob/master/sendmail/datadog_checks/sendmail/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/sendmail/metadata.csv
[6]: https://docs.datadoghq.com/help