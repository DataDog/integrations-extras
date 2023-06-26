# Agent Check: CloudNatix

## Overview

This check provides the data from [CloudNatix][1].

CloudNatix connects to multiple VM & K8s Clusters, enabling automated capacity, cost & operation optimization using patent-pending Autopilot technology. CloudNatix Insights also gives DevOps teams proactive visibility into potential capacity and availability issues, turbocharging productivity.

The CloudNatix integration provides cost and operational optimization insights to DataDog with an out-of-the-box dashboard, allowing you to quickly view cluster cost and analyze opportunities to reduce cost.

## Setup

### Installation

To install the CloudNatix check on your cluster:

1. Build a new Docker image of Datadog agent with installing CloudNatix integration check.
   Please see [here](https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker)
2. [Install the Datadog Agent][3] into your Kubernetes cluster with the built Docker image.
3. [Install CloudNatix][2] into your Kubernetes cluster. CloudNatix clusteragent will
   automatically configure itself to work with the Datadog integration.

### Validation

Once set up, you will see several metrics.  Check the dashboard page
and some graph appears.

## Data Collected

### Metrics

- cloudnatix.compute.daily_spend: the total spend of the cluster recognized by CloudNatix.
- cloudnatix.workload.monthly_spend: the monthly spend of a workload estimated by by CloudNatix.
- cloudnatix.workload.monthly_projected_saving: the monthly saving of a workload
  when autopilot, estimated by CloudNatix.
- cloudnatix.workload.resource: the kubernetes resource requests or limits of a workload.
- cloudnatix.vpa.recommendation: the resource requests for a workload recommended by VPA.
- cloudnatix.vpa: the status of VPA for a workload, e.g. in autopilot mode or not.
- cloudnatix.pod_eviction_by_vpa: the total number of pods evicted by VPA.

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
