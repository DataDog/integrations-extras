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
management ecosystem.  The metrics inform about performance
and resource consumption. This helps validate Universal Crossplane
management cluster sizing and enables optimization.

This check looks for UXP and provider pods by default
in the upbound-system Kubernetes
namespace. The Upbound and provider
pods expose metrics on the `/metrics` URL from port `8080` in
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
```

```
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
```

```
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

The Upbound UXP integration is not included in the [Datadog Agent][2] package, so you need to install it manually.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the check on your host. 

1. Using the Dockerfile example in [Use Community Integrations][3], build a custom image of the Agent that includes the Upbound integration

2. Run the following command to install the Agent integration:

   ``` bash
   datadog-agent integration install -t datadog-upbound-uxp==1.0.0
   ```

### Configuration

1. Edit the `upbound_uxp.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Upbound UXP performance data.

See example configuration parameters below.
```
## Options defined here are available for Upbound UXP integrated instances.
#
init_config:

    ## @param service - string - optional
    ## Attach the tag `service:<SERVICE>` to every metric, event,
    ## and service check emitted by this integration.
    ##
    ## Additionally, this sets the default `service` for every log source.
    #
    # service: <SERVICE>

## Every instance is scheduled independently of the others.
#
instances:

    ## @param min_collection_interval - number - optional - default: 15
    ## This changes the collection interval of the check. For more information, see:
    ## https://docs.datadoghq.com/developers/write_agent_check/#collection-interval
    #
    #
    # min_collection_interval: 15

    ## @param uxp_url - string - optional - default: "/metrics"
    ## This changes at which path metrics are scraped.
    #
    # uxp_url: "/metrics"

    ## @param uxp_port - string - optional - default: "8080"
    ## This changes at which port metrics are scraped.
    #
    # uxp_port: "8080"

    ## @param uxp_hosts - array of strings - optional - default: []
    ## Specifies hosts from which to collect metrics.
    ## Note, the Datadog Agent discovers Crossplane
    ## and provider pods automatically. A usecase is for
    ## out of cluster agent tests.
    #
    # uxp_hosts: [
    #   "localhost"
    # ]

    ## @param verbose - boolean - optional - default: false
    ## The agent provides additonal logging output when
    ## verbose is selected.
    #
    # verbose: false

    ## @param namespace - string - optional - default: upbound-system
    ## The namespace where the Crossplane and Provider pods reside.
    #
    # namespace: "upbound-system"

    ## @params metrics_default - string - optional - default: min
    ## Easy selection of metrics default set. Values can be
    ##  none # indicates no default metrics and implies that custom
    ##       # selection will be provided in "metrics" field.
    ##  min  # indicates opinionated min set
    ##  more # indicates min set plus additional metrics
    ##  max  # indicates all metrics that the Crossplane pod and providers
    ##       # emit will be collected and forwarded to the Datadog
    ##       # organization identified by the Datadog API key specified during
    ##       # agent installation.
    #
    # metrics_default: "min"

    ## @params metrics_ignore_pod_annotations - boolean - optional - default: true
    ## By default the agent determines which metrics to scrape based
    ## on this configuration file. When metrics_ignore_pod_annotations is set
    ## to false, then the agent will also apply pod annotations.
    #
    # metrics_ignore_pod_annotations: true

    ## @params prefix - string - optional - default: ""
    ## Prefix that will be inserted between uxp. and (mapped)
    ## metrics name.
    #
    # metrics_prefix: ""

    ## @params metrics - array of strings - optional - default: []
    ## Specification of individually picked metrics.
    ## For a full list of metrics set metrics_default to "max" and
    ## look at your Datadog metrics explorer in the Datadog console.
    #
    # metrics: [
    #   {"go_goroutines": "company_prefix_go_goroutines"},
    #   # only one value needed when name mapping is not needed
    #   {"go_memstats_heap_alloc_bytes"},
    # ]
```
See [conf.yaml.example][4] for a generic configuration example.

2. [Restart the Agent][5]).

3. Pod Annotations
You may annotate your Crossplane and Provider pods directly with
a subset of the metrics you wish to collect from them.

A sample annotation may look as follows:
```
customAnnotations:
  # Picked up by Universal Crossplane Datadog Integration
  # Pattern to match: ad.datadoghq.com/uxp.<pod-name without pod hash>.instances
  ad.datadoghq.com/uxp.crossplane.instances: |
    [
      {
        "metrics": [
          {"controller_runtime_active_workers": "crossplane_controller_runtime_active_workers"},
          {"controller_runtime_reconcile_errors": "controller_runtime_reconcile_errors_total"},
          {"controller_runtime_reconcile": "controller_runtime_reconcile_total"},
          {"go_gc_duration_seconds": "crossplane_go_gc_duration_seconds"},
          {"go_goroutines": "crossplane_go_goroutines"}
          {"go_memstats_mcache_inuse_bytes": "crossplane_go_memstats_mcache_inuse_bytes"},
          {"go_memstats_mcache_sys_bytes": "crossplane_go_memstats_mcache_sys_bytes"},
          {"go_memstats_mspan_inuse_bytes": "crossplane_go_memstats_mspan_inuse_bytes"},
          {"go_memstats_mspan_sys_bytes": "crossplane_go_memstats_mspan_sys_bytes"},
          {"go_memstats_next_gc_bytes": "crossplane_go_memstats_next_gc_bytes"},
          {"go_memstats_other_sys_bytes": "crossplane_go_memstats_other_sys_bytes"},
          {"go_memstats_stack_inuse_bytes": "crossplane_go_memstats_stack_inuse_bytes"},
          {"go_memstats_stack_sys_bytes": "crossplane_go_memstats_stack_sys_bytes"},
          {"go_memstats_sys_bytes": "crossplane_go_memstats_sys_bytes"},
          {"go_threads": "crossplane_go_threads"},
          {"leader_election_master_status": "crossplane_leader_election_master_status"},
          {"process_cpu_seconds": "crossplane_process_cpu_seconds_total"},
          {"process_max_fds": "crossplane_process_max_fds"},
          {"process_open_fds": "crossplane_process_open_fds"},
          {"process_resident_memory_bytes": "crossplane_process_resident_memory_bytes"},
          {"process_start_time_seconds": "crossplane_process_start_time_seconds"},
          {"process_virtual_memory_bytes": "crossplane_process_virtual_memory_bytes"},
          {"process_virtual_memory_max_bytes": "crossplane_process_virtual_memory_max_bytes"},
          {"rest_client_requests": "crossplane_rest_client_requests_total"},
          {"workqueue_adds": "crossplane_workqueue_adds_total"},
          {"workqueue_depth": "crossplane_workqueue_depth"},
          {"workqueue_retries": "crossplane_workqueue_retries_total"},
          {"workqueue_unfinished_work_seconds": "crossplane_workqueue_unfinished_work_seconds"},
          {"workqueue_work_duration_seconds": "crossplane_workqueue_work_duration_seconds_bucket"}
        ]
      }
    ]
```

### Validation

[Run the Agent's status subcommand][6] and look for `upbound_uxp` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

Upbound UXP does not include any service checks.

### Events

Upbound UXP does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://app.datadoghq.com/integrations/upbound-uxp
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[4]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/datadog_checks/upbound_uxp/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://github.com/DataDog/integrations-extras/blob/master/upbound_uxp/metadata.csv
[11]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
