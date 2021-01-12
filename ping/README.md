# Agent Check: Ping

## Overview

This check uses the system [ping][1] command to test the reachability of a host.
It also optionally measures the round-trip time for messages sent from the check to the destination host.

Ping operates by sending Internet Control Message Protocol (ICMP) echo request packets to the target host and waiting for an ICMP echo reply.

This check uses the system ping command, rather than generating the ICMP echo request itself, as creating an ICMP packet requires a raw socket, and creating raw sockets requires root privileges, which the Agent does not have. The ping command uses the `setuid` access flag to run with elevated privileges, avoiding this issue.

## Setup

The Ping check is **NOT** included in the [Datadog Agent][2] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Ping check on your host. See our dedicated Agent guide for [installing community integrations][6] to install checks with the [Agent prior to version 6.8][3] or the [Docker Agent][4]:

1. [Download and launch the Datadog Agent][2].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
      datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `ping.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your ping performance data. See the [sample ping.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `ping` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Service Checks

**`network.ping.can_connect`**:

Returns `CRITICAL` if the Agent cannot communicate with the target host. Returns `OK` if the ping is successful.

### Events

The Ping check does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://en.wikipedia.org/wiki/Ping_(networking_utility)
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/ping/datadog_checks/ping/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/ping/metadata.csv
[11]: https://docs.datadoghq.com/help/
