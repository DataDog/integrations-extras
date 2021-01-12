# Agent Check: kernelcare

## Overview

[KernelCare][1] is a live patching system that automatically applies security patches to Linux kernel vulnerabilities, with no reboots. It’s used on over 500,000 servers, and has been used to patch servers running for 6+ years for Dell, Zoom and other enterprise companies. It works with all major Linux distributions, such as RHEL, CentOS, Amazon Linux, and Ubuntu & interoperates with common vulnerability scanners, cloud monitoring tools & patch management solutions.

This integration allows you to forward the Kernelcare metrics through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the HBase RegionServer check on your host. See our dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior v6.8][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][6].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-<INTEGRATION_NAME>==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][7].
### Configuration

1. Edit the `kernelcare.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your kernelcare performance data. See the [sample kernelcare.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `kernelcare` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Service Checks

**`kernelcare.can_connect`**:

Returns `Critical` if the Agent cannot connect to Kernelcare to collect metrics, returns `OK` otherwise.

### Events

kernelcare does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://www.kernelcare.com
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://github.com/DataDog/integrations-extras/blob/master/kernelcare/datadog_checks/kernelcare/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[11]: https://github.com/DataDog/integrations-extras/blob/master/kernelcare/metadata.csv
[12]: https://docs.datadoghq.com/help/
