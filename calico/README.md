# Agent Check: Calico

## Overview

This check monitors [Calico][1] through the Datadog Agent.

The Calico check sends metrics concerning network and security in a Kubernetes cluster set up with Calico.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions. A setup using Autodiscovery Integration is also below.

### Installation with a Kubernetes cluster-based Agent

Using annotations:

1. Set up Calico on your cluster if you have not already.

2. Enable Prometheus metrics using the instructions in [Monitor Calico component metrics][9].
   Once enabled, you should have a `felix-metrics-svc` service running in your cluster, as well as a `prometheus-pod`.

3. To use Autodiscovery, modify `prometheus-pod`. Add the following snippet to your Prometheus YAML configuration file:

```
metadata:
  [...]
  annotations:
   ad.datadoghq.com/prometheus-pod.check_names: |
   ["openmetrics"]
   ad.datadoghq.com/prometheus-pod.init_configs: |
   [{}]
   ad.datadoghq.com/prometheus-pod.instances: |
     [
        {
           "prometheus_url": "http://<FELIX-SERVICE-IP>:<FELIX-SERVICE-PORT>/metrics",
           "namespace": "calico",
           "metrics": ["*"]
        }
     ]
  spec:
    [....]
```

You can find values for `<FELIX-SERVICE-IP>` and `<FELIX-SERVICE-PORT>` by running `kubectl get all -all-namespaces`.

### Installation with an OS-based Agent

To install the Calico check on your host:

1. Install Datadog's [developer toolkit][10] on your machine.

2. Run `ddev release build calico` to build the package.

3. [Download the Datadog Agent][11].

4. Upload the build artifact to any host with an Agent and
   run `datadog-agent integration install -w path/to/calico/dist/<ARTIFACT_NAME>.whl`.

5. Follow [Monitor Calico component metrics][9] until you have a `felix-metrics-svc` service running using `kubectl get all --all-namespaces`.

6. If you are using minikube, you must forward port 9091 to `felix-metrics-svc`.
   Run `kubectl port-forward service/felix-metrics-svc 9091:9091 -n kube-system`.

   If you are not using minikube, check that `felix-metrics-svc` has an external IP. If the service does not have an external IP, use `kubectl edit svc` to change its type from `ClusterIP` to `LoadBalancer`.

Once installation is complete, you can continue to configuration (see below).

### Configuration for host based setup

1. Edit the `calico.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Calico performance data. The only required parameter is the `openmetrics_endpoint` URL. See the [sample calico.d/conf.yaml][3] for all available configuration options.

2. If you are using minikube, use 'http://localhost:9091/metrics' as your `openmetrics_endpoint` URL.
   If you are not using minikube, use `http://<FELIX-METRICS-SVC-EXTERNAL-IP>:<PORT>/metrics` as your `openmetrics_endpoint` URL.

3. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `calico` under the Checks section.

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Events

The Calico integration does not include any events.

### Service Checks

See [service_checks.json][7] for a list of service checks provided by this integration.

## Concerning logs

Since Calico structure is set up in a Kubernetes cluster, it is built with deployments, pods, and services.
The Kubernetes integration fetches logs from containers. Therefore, when Kubernetes integration is set up, Calico logs are automatically available in the Datadog Log Explorer.

## Troubleshooting

Need help? Contact [Datadog support][8].

[1]: https://www.tigera.io/project-calico/
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/calico/datadog_checks/calico/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/calico/metadata.csv
[7]: https://github.com/DataDog/integrations-core/blob/master/calico/assets/service_checks.json
[8]: https://docs.datadoghq.com/help/
[9]: https://docs.projectcalico.org/maintenance/monitor/monitor-component-metrics
[10]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[11]: https://app.datadoghq.com/account/settings#agent
