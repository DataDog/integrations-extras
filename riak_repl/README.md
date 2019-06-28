# Agent Check: Riak-Repl

## Overview

This check monitors Riak replication [riak-repl][1].

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Riak-Repl check on your host. See our dedicated Agent guide about [how to install Community integration][2] to see how to install them with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `riak_repl` package, run:

    ```
    ddev -e release build riak_repl
    ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_RIAK_REPL_ARTIFACT_>/<RIAK_REPL_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][7].
8. [Restart the Agent][8].

### Configuration

1. Edit the `riak_repl.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your riak_repl performance data. See the [sample riak_repl.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

### Validation

[Run the Agent's `status` subcommand][11] and look for `riak_repl` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this integration.

### Service Checks

riak_repl does not currently include any service checks.

### Events

riak_repl does not currently include any events.

## Troubleshooting

Need help? Contact [Datadog support][13].

[1]: https://docs.datadoghq.com/integrations/riak_repl
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#restart-the-agent
[9]: https://github.com/DataDog/integrations-extras/blob/master/riak_repl/datadog_checks/riak_repl/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[12]: https://github.com/DataDog/integrations-extras/blob/master/riak_repl/metadata.csv
[13]: https://docs.datadoghq.com/help
