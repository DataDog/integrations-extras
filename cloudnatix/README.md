# Agent Check: CloudNatix

## Overview

This check provides the data from [CloudNatix][1].

## Setup

### Installation

To install the CloudNatix check on your cluster:

1. [Install CloudNatix](https://docs.cloudnatix.com/docs/tutorial) into your cluster.

2. [Download the Datadog Agent][2].

### Configuration

There is no configuration at this time.

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
[2]: https://app.datadoghq.com/account/settings#agent/kubernetes
[3]: https://docs.datadoghq.com/help/
[4]: support@cloudnatix.com
