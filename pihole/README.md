# Agent Check: pihole

## Overview

This check monitors [Pi-hole][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the Pi-hole check on your host:

1. Install the [developer toolkit][3] on any machine.
2. Run `ddev release build pihole` to build the package.
3. [Download the Datadog Agent][4].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/pihole/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `pihole.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Pi-hole performance data. See the [sample pihole.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `pihole` under the Checks section.


### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

**`pihole.running`**:

Returns `CRITICAL` if the Agent cannot communicate with the target host. Returns `OK` if the connection to Pi-hole is successful.

### Events

Pi-hole does not include any events.

[1]: https://pi-hole.net/
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://github.com/DataDog/integrations-extras/blob/master/pihole/datadog_checks/pihole/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/pihole/metadata.csv




