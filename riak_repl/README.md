# Agent Check: Riak-Repl

## Overview

This check monitors Riak replication [riak-repl][1].

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Riak-Repl check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]: your `ddev` config with the `integrations-extras/` path:

1. [Download and launch the Datadog Agent][5].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `riak_repl.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your riak_repl performance data. See the [sample riak_repl.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8]

### Validation

[Run the Agent's `status` subcommand][9] and look for `riak_repl` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

riak_repl does not currently include any service checks.

### Events

riak_repl does not currently include any events.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://docs.datadoghq.com/integrations/riak_repl/
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/riak_repl/datadog_checks/riak_repl/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/riak_repl/metadata.csv
[11]: https://docs.datadoghq.com/help/
