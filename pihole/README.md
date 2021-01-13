# Agent Check: pihole

## Overview

This check monitors [Pi-hole][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Pi-hole check on your host. See the dedicated Agent guide for [installing community integrations][6] to install checks with the [Agent prior to version 6.8][3] or the [Docker Agent][4]:

1. [Download the Datadog Agent][4].

2. Run the following command to install the integrations wheel with the Agent:

   ```shell
      datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `pihole.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Pi-hole performance data. See the [sample pihole.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `pihole` under the Checks section.


### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Service Checks

**`pihole.running`**:

Returns `CRITICAL` if the Agent cannot communicate with the target host. Returns `OK` if the connection to Pi-hole is successful.

### Events

Pi-hole does not include any events.

[1]: https://pi-hole.net/
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://github.com/DataDog/integrations-extras/blob/master/pihole/datadog_checks/pihole/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/pihole/metadata.csv



