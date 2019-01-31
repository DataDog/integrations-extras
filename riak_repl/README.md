# Agent Check: Riak-Repl

## Overview

This check monitors Riak replication [riak-repl][1].

## Setup

### Installation

The riak-repl check is not included in the [Datadog Agent][2] package, so you will need to install it yourself.

### Configuration

1. Edit the `riak_repl.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your riak_repl performance data. See the [sample riak_repl.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4]

### Validation

[Run the Agent's `status` subcommand][5] and look for `riak_repl` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Service Checks

riak_repl does not currently include any service checks.

### Events

riak_repl does not currently include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://docs.datadoghq.com/integrations/riak_repl/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://github.com/DataDog/integrations-extras/blob/master/riak_repl/datadog_checks/riak_repl/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[5]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[6]: https://docs.datadoghq.com/help/
[7]: https://github.com/DataDog/integrations-extras/blob/master/riak_repl/metadata.csv
