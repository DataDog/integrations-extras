# Agent Check: Upbound UXP

## Overview

Upbound provides a control plane framework for businesses
to accelerate their journey building custom clouds on top
of arbitrary cloud resources, making the process quicker, more flexible, and reducing cognitive load for users. With Upbound, users can reduce risk and make themselves audit-ready by enforcing governance and compliance with the Universal Crossplane.

Universal Crossplane users can offer
their own internal cloud API to their teams through
composite resource definitions. Their
custom cloud service can then map that API to downstream providers.
The providers create and manage the lifecycle of the external
cloud resources orchestrated through Universal
Crossplane when a user claims resources.
Amazon AWS, Microsoft Azure, and Google
GCP are out of the box supported cloud providers.

This Datadog integration facilitates the monitoring
of Universal Crossplane and provider Kubernetes pods.
Metrics are sent from Upbound's pods in the self hosted
customer environment to the customer's Datadog account.
They track the health of this self-managed
infrastructure provisioning and resource lifecycle
management ecosystem.

The metrics inform about performance
and resource consumption. This helps validate Universal Crossplane
management cluster sizing and enables optimization.

The checks monitor [Upbound UXP](https://docs.upbound.io/uxp/)
related metrics. It looks for UXP and provider pods by default
in the upbound-system Kubernetes
namespace. The Upbound and provider
pods emit metrics at port 8080/metrics in
a Prometheus compatible format.

## Setup

### Prerequisites

The Datadog agent requires permissions to discover UXP and provider pods.
Create a service account, a cluster role, and a cluster role binding
to grant those permissions following the example below.

Note that the Datadog agent in the configuration
below resides in an arbitrary `monitoring` namespace.
Your agent may reside in a namespace of your choice.
Configure the service account and cluster role accordingly.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: datadog-upbound
  namespace: monitoring
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: apiserver-cluster-role
  namespace: monitoring
rules:
  - apiGroups:
      - ""
    resources:
      - pods
    verbs: ["get", "list" ]
  - nonResourceURLs: ["/metrics"]
    verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: apiserver-cluster-role-binding
subjects:
- namespace: monitoring
  kind: ServiceAccount
  name: datadog-upbound
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: apiserver-cluster-role
```

### Installation

To install the Upbound UXP check on your host:


1. Install the [developer toolkit][11] on any machine.

2. Run `ddev release build upbound_uxp` to build the package.

3. Upload the build artifact to any host with an Agent and run
```
datadog-agent integration install
  -w path/to/upbound_uxp/dist/<ARTIFACT_NAME>.whl
```

OR

Copy the build artifact to an agent container,
that may be running in Kubernetes with the following command.
```
kubectl -n <MONITORING_NAMESPACE>
  cp path/to/upbound_uxp/dist/<ARTIFACT_NAME>.whl
     <DATADOG_CONTAINER_NAME>:<PATH_TO_DIST_IN_CONTAINER>
```

4. Install it with
```
kubectl -n <MONITORING_NAMESPACE> exec
  -it <DATADOG_CONTAINER_NAME>
  -- agent integration install -w -r
     <PATH_TO_DIST_IN_CONTAINER>/<ARTIFACT_NAME>.whl`
```

### Configuration

1. Edit the `upbound_uxp/conf.yaml` file, in the `conf.d` folder
at the root of your Agent's configuration directory to start
collecting your upbound_uxp performance data. See the
[sample upbound_uxp/conf.yaml][4]
for available configuration options.

2. Restart the Agent.

### Validation

[Run the Agent's status subcommand] and look for `upbound_uxp`
under the Checks section.

Run tests as follows:
```
DDEV_SKIP_GENERIC_TAGS_CHECK=True ddev test upbound_uxp
```

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

Upbound UXP does not include any service checks.

### Events

Upbound UXP does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/datadog_checks/upbound_uxp/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/metadata.csv
[11]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
