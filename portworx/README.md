# Portworx Integration

## Overview

Get metrics from Portworx service in real time to:

- Monitor health and performance of your Portworx cluster
- Track disk usage, latency, and throughput for Portworx volumes
- Set up [Autopilot rules][12]

## Setup

### Installation

#### Create the Datadog credentials Secret

Create a Kubernetes Secret containing your Datadog API and application keys:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: datadog-credentials
  namespace: datadog-ns
type: Opaque
data:
  # Base64-encoded Datadog API Key
  api-key: <base64-encoded-api-key>
  # Base64-encoded Datadog Application Key
  app-key: <base64-encoded-app-key>
```

- Replace the namespace, secret name, and encoded key values as required.
- Use an application key with metrics read permission for `app-key`.

#### Configure the Datadog Agent to export Portworx metrics

Create a Datadog Agent values file (for example, `datadog_config.yaml`):

```yaml
datadog:
  site: "datadoghq.com"
  clusterName: "your-cluster-name"
  apiKeyExistingSecret: "datadog-credentials"
  kubelet:
    tlsVerify: false
  clusterChecks:
    enabled: true
  orchestratorExplorer:
    enabled: true
clusterAgent:
  enabled: true
  admissionController:
    enabled: true
    mutateUnlabelled: false
```

Use your own `site`, `clusterName`, and `apiKeyExistingSecret`. The Agent scrapes Portworx metrics and sends them to Datadog.

Install the Datadog Agent with Helm:

```shell
helm repo add datadog https://helm.datadoghq.com
helm upgrade --install datadog-agent datadog/datadog -f ./datadog_config.yaml
```

### Configuration

#### Annotate Portworx, Stork, and Autopilot pods

Configure Datadog Autodiscovery annotations so the Agent knows which endpoints to scrape. The typical Prometheus-style service endpoints are:

| Component | Endpoint | Metrics filter |
|-----------|----------|----------------|
| Portworx API | `http://%%host%%:17001/metrics` | `px_*` |
| Stork | `http://%%host%%:9091/metrics` | `stork_*` |
| Autopilot | `http://%%host%%:9628/metrics` | `autopilot_*` |

> **Note:** Portworx has many metrics. For most use cases, Portworx API metrics alone are sufficient.

Apply a `ComponentK8sConfig` Custom Resource (CR) to add the annotations:

```yaml
apiVersion: core.libopenstorage.org/v1
kind: ComponentK8sConfig
metadata:
  name: datadog-components-config
  namespace: portworx
spec:
  components:
  - componentNames:
    - Portworx API
    workloadConfigs:
    - workloadNames:
      - portworx-api
      annotations:
        ad.datadoghq.com/portworx-api.checks: |-
          {
            "openmetrics": {
              "instances": [
                {
                  "openmetrics_endpoint": "http://%%host%%:17001/metrics",
                  "namespace": "portworx",
                  "metrics": ["px_*"]
                }
              ]
            }
          }
  - componentNames:
    - Stork
    workloadConfigs:
    - workloadNames:
      - stork
      annotations:
        ad.datadoghq.com/stork.checks: |-
          {
            "openmetrics": {
              "instances": [
                {
                  "openmetrics_endpoint": "http://%%host%%:9091/metrics",
                  "namespace": "portworx",
                  "metrics": ["stork_*"]
                }
              ]
            }
          }
  - componentNames:
    - Autopilot
    workloadConfigs:
    - workloadNames:
      - autopilot
      annotations:
        ad.datadoghq.com/autopilot.checks: |-
          {
            "openmetrics": {
              "instances": [
                {
                  "openmetrics_endpoint": "http://%%host%%:9628/metrics",
                  "namespace": "portworx",
                  "metrics": ["autopilot_*"]
                }
              ]
            }
          }
```

At this point, the Datadog Agent is configured to scrape Portworx metrics and the Portworx, Stork, and Autopilot pods are annotated for Autodiscovery.
You can verify the Agent is scraping metrics by running `kubectl exec <datadog-agent-pod> -n datadog-ns -- agent status` and looking for `portworx` in the `Checks` section.

To configure rules, see the [Autopilot documentation][12].

### Validation

Run the following command to confirm the Agent is scraping Portworx metrics:

```shell
kubectl exec <datadog-agent-pod> -n <datadog-namespace> -- agent status
```

Look for `openmetrics` instances under the `Checks` section with `portworx`, `stork`, and `autopilot`.

## Compatibility

This integration is compatible with Portworx 1.4.0 and later versions.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration. For a full reference of all Portworx metrics, see the [Portworx Metrics Reference][13].

### Events

The Portworx integration does not include any events.

### Service Checks

The Portworx integration does not include any service checks.

## Troubleshooting

### Agent cannot scrape metrics

If metrics are not appearing in Datadog, check the following:

- Verify the `ComponentK8sConfig` CR was applied and the pods have the expected annotations:
  ```shell
  kubectl get pod <portworx-api-pod> -n portworx -o jsonpath='{.metadata.annotations}'
  ```
- Confirm the OpenMetrics endpoints are reachable from within the Agent pod:
  ```shell
  kubectl exec <datadog-agent-pod> -n <datadog-namespace> -- curl http://<node-ip>:17001/metrics
  ```
- Check Agent logs for scrape errors:
  ```shell
  kubectl logs <datadog-agent-pod> -n <datadog-namespace>
  ```

## Further Reading

Additional helpful documentation, links, and articles:

- [Monitoring multi-cloud container storage with Portworx and Datadog][11]

## Support

Need help? Contact [Portworx support](mailto:support@purestorage.com).


[10]: https://github.com/DataDog/integrations-extras/blob/master/portworx/metadata.csv
[11]: https://www.datadoghq.com/blog/portworx-integration/
[12]: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot
[13]: https://docs.portworx.com/portworx-enterprise/reference/metrics#storage-pool-metrics
