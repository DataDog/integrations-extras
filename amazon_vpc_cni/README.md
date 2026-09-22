# Agent Check: Amazon VPC CNI

## Overview

The [Amazon VPC CNI plugin for Kubernetes][13] is the networking plugin deployed on each Amazon EC2 node in an Amazon EKS cluster. It manages elastic network interfaces (ENIs) and assigns private IPv4 or IPv6 addresses from the VPC to each pod.

This integration scrapes the Prometheus metrics exposed by the VPC CNI plugin (`awscni_*`) and provides visibility into IP address allocation, ENI usage, AWS API activity, and IPAMD health. It lets you replace ad-hoc `awscni_*` custom metrics with an official, curated integration.

## Setup

### Installation

If you are using Datadog Agent v6.8+, follow the instructions below to install the Amazon VPC CNI check on your host. See the dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent Manager][2] or in a [Docker environment][4].

1. [Download and launch the Datadog Agent][3].
2. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-amazon-vpc-cni==<INTEGRATION_VERSION>
   ```

3. Configure your integration in the same way as core [integrations][5].

### Configuration

Enable Prometheus metrics on the `aws-node` DaemonSet by setting the environment variable `ENABLE_PROMETHEUS_METRICS` to `true`. The plugin then exposes metrics at `http://localhost:61678/metrics` on each node.

1. Edit the `amazon_vpc_cni.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your Amazon VPC CNI metrics. See the [sample amazon_vpc_cni.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `amazon_vpc_cni` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

The Amazon VPC CNI integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[2]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#start-stop-and-restart-the-agent
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/amazon_vpc_cni/datadog_checks/amazon_vpc_cni/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/amazon_vpc_cni/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/amazon_vpc_cni/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/aws/amazon-vpc-cni-k8s
