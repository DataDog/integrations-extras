# Agent Check: Ping

## Overview

This check uses the system [ping][1] command to test the reachability of a host.
It also optionally measures the round-trip time for messages sent from the check to the
destination host.

Ping operates by sending Internet Control Message Protocol (ICMP) echo request packets
to the target host and waiting for an ICMP echo reply.

This check uses the system ping command, rather than generating the ICMP echo request
itself, as creating an ICMP packet requires a raw socket, and creating raw sockets
requires root privileges, which the agent does not have. The ping command uses the
`setuid` access flag to run with elevated privileges, avoiding this issue.

## Setup

### Installation

The Ping check is not included in the [Datadog Agent][2] package, so you need to
install it yourself.

### Configuration

1. Edit the `ping.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your ping performance data.
   See the [sample ping.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `ping` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

**`network.ping.can_connect`**:

Returns DOWN if the check does not receive a response from `host`, otherwise UP.

### Events

Ping does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://en.wikipedia.org/wiki/Ping_(networking_utility)
[2]: https://github.com/DataDog/integrations-core/blob/master/ping/datadog_checks/ping/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help/
[6]: https://github.com/DataDog/integrations-extras/blob/master/ping/metadata.csv
