# Agent Check: Ping

## Overview

This check uses the system [ping][1] command to test the reachability of a host.
It also optionally measures the round-trip time for messages sent from the check to the destination host.

Ping operates by sending Internet Control Message Protocol (ICMP) echo request packets to the target host and waiting for an ICMP echo reply.

This check uses the system ping command, rather than generating the ICMP echo request itself, as creating an ICMP packet requires a raw socket. Creating raw sockets requires root privileges, which the Agent does not have. The ping command uses the `setuid` access flag to run with elevated privileges, avoiding this issue.

## Setup

The ping check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the ping check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the one following commands to install the Agent integration:

   ```shell
   # Linux
   datadog-agent integration install -t datadog-ping==<INTEGRATION_VERSION>
   
   # Windows
   agent.exe integration install -t datadog-ping==<INTEGRATION_VERSION>
   ```
2. Install the `ping` binary in accordance to your OS. For example, run the following command for Ubuntu:
   ```shell
   apt-get install iputils-ping
   ```
   
3. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `ping.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your ping performance data. See the [sample ping.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

Run the [Agent's status subcommand][9] and look for `ping` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Events

The Ping check does not include any events.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

## Troubleshooting

### `SubprocessOutputEmptyError: get_subprocess_output expected output but had none` Error
While running the Ping integration, you may see an error like the following:

```
      Traceback (most recent call last):
        File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/base/checks/base.py", line 1006, in run
          self.check(instance)
        File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/ping/ping.py", line 65, in check
          lines = self._exec_ping(timeout, host)
        File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/ping/ping.py", line 48, in _exec_ping
          lines, err, retcode = get_subprocess_output(
        File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/base/utils/subprocess_output.py", line 56, in get_subprocess_output
          out, err, returncode = subprocess_output(cmd_args, raise_on_empty_output, env=env)
      _util.SubprocessOutputEmptyError: get_subprocess_output expected output but had none.
```

Because the Ping integration is not included by default in the Agent, the `ping` binary is also not included with the Agent. You must install the `ping` binary yourself in order to run the integration successfully. 


Need help? Contact [Datadog support][11].


[1]: https://en.wikipedia.org/wiki/Ping_%28networking_utility%29
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/ping/datadog_checks/ping/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/ping/metadata.csv
[11]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/ping/assets/service_checks.json
