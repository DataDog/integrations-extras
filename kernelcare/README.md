# Agent Check: kernelcare

## Overview

[KernelCare][1] is a live patching system that automatically applies security patches to Linux kernel vulnerabilities, with no reboots. It's used on over 500,000 servers, and has been used to patch servers running for 6+ years for Dell, Zoom and other enterprise companies. It works with all major Linux distributions, such as RHEL, CentOS, Amazon Linux, and Ubuntu & interoperates with common vulnerability scanners, cloud monitoring tools & patch management solutions.

This integration allows you to forward the Kernelcare metrics through the Datadog Agent.

## Setup

The Kernelcare check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Kernelcare check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-kernelcare==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `kernelcare.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your kernelcare performance data. See the [sample kernelcare.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `kernelcare` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Events

kernelcare does not include any events.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].


[1]: https://www.kernelcare.com
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://github.com/DataDog/integrations-extras/blob/master/kernelcare/datadog_checks/kernelcare/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[11]: https://github.com/DataDog/integrations-extras/blob/master/kernelcare/metadata.csv
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/kernelcare/assets/service_checks.json
