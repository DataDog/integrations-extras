# Agent Check: Calico

## Overview

This check monitors [calico][1] through the Datadog Agent.

The Calico check sends metrics concerning network and security in a Kubernetes cluster set up with Calico.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions. There will also be a setup below using Autodiscovery Integration.

### Installation with kubernetes cluster based agent

Using kubernetes cluster based agent, using annotations :

1. Check that you have a cluster with calico set up on it.

2. Enable prometheus metrics following [Calico doc](https://docs.projectcalico.org/maintenance/monitor/monitor-component-metrics)
   You should have a felix-metrics-svc service running in your cluster, as well as a prometheus-pod.

To use autodiscovery, we are going to modify prometheus-pod.

3. Add the following snippet to your prometheus yaml file :

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

You can find <FELIX-SERVICE-IP> && <FELIX-SERVICE-PORT> using kubectl get all —all-namespaces.

### Installation with OS based agent

Using OS based DD Agent :

To install the calico check on your host:

1. Install the [developer toolkit]
   (https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
   on any machine.

2. Run `ddev release build calico` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and
   run `datadog-agent integration install -w path/to/calico/dist/<ARTIFACT_NAME>.whl`.

5. Follow [Calico doc](https://docs.projectcalico.org/maintenance/monitor/monitor-component-metrics) until you have felix-metrics-svc running using `kubectl get all --all-namespaces`

6. If you are using minikube, you have to use `kubectl port-forward` to forward port 9091 to felix-metrics-svc. (Your command should look like `kubectl port-forward service/felix-metrics-svc 9091:9091 -n kube-system`)

7. If you're not using minikube, you can check that felix-metrics-svc has an external IP. If not, you may change its type from ClusterIP to LoadBalancer.

8. You can now configure the integration

### Configuration for host based setup

1. Edit the `calico.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your calico performance data. See the [sample calico.d/conf.yaml][3] for all available configuration options.

2. If you're using minikube, use 'http://localhost:9091/metrics' as prometheus url. Else, you can use "http://<FELIX-METRICS-SVC-EXTERNAL-IP>:<PORT>/metrics" as prometheus url.

3. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `calico` under the Checks section.

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Events

The calico integration does not include any events.

### Service Checks

The calico integration does not include any service checks.

See [service_checks.json][7] for a list of service checks provided by this integration.

## Concerning logs

Since Calico structure is setup in a kubernetes cluster, it is built with deployments, pods, service.
Kubernetes makes a great job at fetching logs from the corresponding services, and therefore, by using Kubernetes integration
along with calico, logs are automatically available in datadoghq Log section.

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
