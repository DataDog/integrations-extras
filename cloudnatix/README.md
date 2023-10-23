# Agent Check: CloudNatix

## Overview

This check provides data from [CloudNatix][1].

CloudNatix connects to multiple VM-based and Kubernetes clusters, enabling automated capacity, cost, and operation optimization with patent-pending Autopilot technology. CloudNatix Insights gives DevOps teams proactive visibility into potential capacity and availability issues.

The CloudNatix integration provides cost and operational optimization insights to Datadog with an out-of-the-box dashboard, allowing you to quickly view cluster cost and analyze opportunities to reduce cost.

## Setup

### Installation

To install the CloudNatix check on your cluster:

1. Build a Docker image of the Datadog Agent that has the CloudNatix integration check installed. For more information, see [Use Community Integrations][7].
2. [Install the Datadog Agent][2] into your Kubernetes cluster with the built Docker image.
3. [Install CloudNatix][3] into your Kubernetes cluster. The CloudNatix Cluster Agent will
   automatically configure itself to work with the Datadog integration.

### Validation

[Run the Agent's status subcommand][4] and look for `cloudnatix` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.

### Service Checks

CloudNatix does not include any service checks.

### Events

CloudNatix does not include any events.

## Troubleshooting

Need help? Contact [Cloudnatix support][6].

## Further Reading

Additional helpful documentation, links, and articles:

- [Optimize your infrastructure with CloudNatix and Datadog][8]

[1]: https://cloudnatix.com/
[2]: https://app.datadoghq.com/account/settings#agent/kubernetes
[3]: https://docs.cloudnatix.com/docs/tutorial
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/cloudnatix/metadata.csv
[6]: mailto:support@cloudnatix.com
[7]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[8]: https://www.datadoghq.com/blog/infrastructure-optimization-rightsizing-cloudnatix-datadog/
