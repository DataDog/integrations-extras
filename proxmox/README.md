# Agent Check: Proxmox

## Overview

This check monitors [Proxmox][1] through the Datadog Agent. 

The Proxmox check collects metrics from the Proxmox API and sends them to Datadog, providing insight into the performance of your Proxmox virtual machines and hosts.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

The Proxmox check is included in the [Datadog Agent][2] package.
No additional installation is needed on your server.
To install the Proxmox integration, run the following Agent installation command and the steps below. For more information, see the [Integration Management](https://docs.datadoghq.com/agent/guide/integration-management/?tab=linux#install) documentation.

```shell
datadog-agent integration install datadog-vsphere==3.6.0
```


### Configuration

1. Edit the `proxmox.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your proxmox performance data. See the [sample proxmox.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `proxmox` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The Proxmox integration does not include any events.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://proxmox.com
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-core/blob/master/proxmox/datadog_checks/proxmox/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-core/blob/master/proxmox/metadata.csv
[8]: https://github.com/DataDog/integrations-core/blob/master/proxmox/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
