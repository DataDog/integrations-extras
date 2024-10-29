# Scaphandre

## Overview

This check monitors [Scaphandre][1], a monitoring agent that uses RAPL and MsrRAPL via powercap to measure power usage of bare metal machines. The goal of the project is to permit to any company or individual to measure the power consumption of its tech services and get this data in a convenient form, sending it through any monitoring or data analysis toolchain.

## Setup

### Installation

To install the Scaphandre check on your host:


1. Install the developer toolkit [10] on any machine. The specific developer toolkit that should be installed depends on your platform and architecture.

2. Run the following command to build the package:
    ```
    ddev release build scaphandre
    ```

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and run the following command:
    ```
    datadog-agent integration install -w path/to/scaphandre/dist/<ARTIFACT_NAME>.whl
    ```

### Configuration

Edit the `scaphandre.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][5]. See the [sample scaphandre.d/conf.yaml][6] for all available configuration options. For example, to secure Scaphandre command line tags and prevent sensitive data from being pulled into Datadog, use the `exclude_labels` config option.

[Restart the Agent][7] to start sending Scaphandre metrics to Datadog.

### Validation

Run the [Agent's status subcommand][8] and look for `scaphandre` in the **Checks** section.

## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this check.

### Service Checks

Scaphandre does not include any service checks.

### Events

Scaphandre does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://github.com/hubblo-org/scaphandre
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://docs.datadoghq.com/help/
[5]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[6]: https://github.com/DataDog/integrations-core/blob/master/scaphandre/datadog_checks/scaphandre/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[9]: https://github.com/DataDog/integrations-extras/blob/master/scaphandre/metadata.csv
[10]: https://docs.datadoghq.com/developers/integrations/python/
