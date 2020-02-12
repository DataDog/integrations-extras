# Agent Check: Unbound

## Overview

This check monitors [Unbound][1] through the Datadog Agent.

Get metrics from unbound service in real time to:

- Visualize and monitor unbound states

## Setup

### Installation

The Unbound check is **NOT** included in the [Datadog Agent][2] package.

To install the Unbound check on your host:

1. Install the [developer toolkit][3] on any machine.
2. Run `ddev release build unbound` to build the package.
3. [Install the Datadog Agent][4].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/unbound/dist/<ARTIFACT_NAshellME>.whl`.

### Configuration

1. Edit the `unbound.d/conf.yaml` file, in the `conf.d/` folder at the root of
   your Agent's configuration directory to start collecting unbound metrics. See
   the [sample unbound.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `unbound` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.

### Service Checks

**unbound.can_get_stats**
Returns CRITICAL if unbound-control fails or there's an error parsing its output. Returns OK otherwise.

### Events

The Unbound check does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://nlnetlabs.nl/documentation/unbound/unbound-control/
[2]: https://docs.datadoghq.com/agent
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://github.com/DataDog/integrations-extras/blob/master/unbound/datadog_checks/unbound/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/unbound/metadata.csv
[9]: https://docs.datadoghq.com/help
