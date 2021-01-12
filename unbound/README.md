# Agent Check: Unbound

## Overview

This check monitors [Unbound][1] through the Datadog Agent.

Get metrics from unbound service in real time to:

- Visualize and monitor unbound states

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Unbound check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior to version 6.8][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][2].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```
3. Configure your integration like [any other packaged integration][5].

### Configuration

1. Edit the `unbound.d/conf.yaml` file, in the `conf.d/` folder at the root of
   your Agent's configuration directory to start collecting unbound metrics. See
   the [sample unbound.d/conf.yaml][6] for all available configuration options.

2. [Restart the Agent][7].

### Validation

[Run the Agent's status subcommand][8] and look for `unbound` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this integration.

### Service Checks

**unbound.can_get_stats**
Returns CRITICAL if unbound-control fails or there's an error parsing its output. Returns OK otherwise.

### Events

The Unbound check does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][10].

[1]: https://nlnetlabs.nl/documentation/unbound/unbound-control/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://github.com/DataDog/integrations-extras/blob/master/unbound/datadog_checks/unbound/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[9]: https://github.com/DataDog/integrations-extras/blob/master/unbound/metadata.csv
[10]: https://docs.datadoghq.com/help/
