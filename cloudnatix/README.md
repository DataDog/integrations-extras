# Agent Check: CloudNatix

## Overview

This check provides the data from [CloudNatix][1].

CloudNatix connects to multiple VM & K8s Clusters, enabling automated capacity, cost & operation optimization using patent-pending Autopilot technology. CloudNatix Insights also gives DevOps teams proactive visibility into potential capacity and availability issues, turbocharging productivity.

The CloudNatix integration provides cost and operational optimization insights to DataDog with an out-of-the-box dashboard, allowing you to quickly view cluster cost and analyze opportunities to reduce cost.

## Setup

### Installation

To install the CloudNatix check on your cluster:

1. Build a new Docker image of Datadog agent that has the CloudNatix integration check installed.
      * Please see [here](https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker) for details.
2. [Install the Datadog Agent][3] into your Kubernetes cluster with the built Docker image.
3. [Install CloudNatix][2] into your Kubernetes cluster. CloudNatix clusteragent will
   automatically configure itself to work with the Datadog integration.

### Validation

Once set up, you will see several metrics.  Check the dashboard page
and some graph appears.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.

### Service Checks

CloudNatix does not include any service checks.

### Events

CloudNatix does not include any events.

## Troubleshooting

Need help? Contact [Cloudnatix support][4].

[1]: https://cloudnatix.com/
[2]: https://docs.cloudnatix.com/docs/tutorial
[3]: https://app.datadoghq.com/account/settings#agent/kubernetes
[4]: support@cloudnatix.com
