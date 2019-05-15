# Agent Check: Unbound

## Overview

This check monitors [Unbound][1] through the Datadog Agent.

Get metrics from unbound service in real time to:

* Visualize and monitor unbound states
* Be notified about unbound failovers and events.

## Setup

### Installation

The Unbound check is not included in the [Datadog Agent][2] package, so it must
be installed manually.

### Configuration

1. Edit the `unbound.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your unbound performance data. See the [sample unbound.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `unbound` under the Checks section.

## Data Collected

### Metrics

Unbound does not include any metrics.

### Service Checks

Unbound does not include any service checks.

### Events

Unbound does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://nlnetlabs.nl/documentation/unbound/unbound-control/
[2]: https://github.com/DataDog/integrations-core/blob/master/unbound/datadog_checks/unbound/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[5]: https://docs.datadoghq.com/help
