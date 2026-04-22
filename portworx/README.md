# Portworx Integration

## Overview

Get metrics from Portworx service in real time to:

- Monitor health and performance of your Portworx Cluster
- Track disk usage, latency and throughput for Portworx volumes
- Setup Autopilto Rules https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot

## Setup

### Installation

#### Step 1 – Create Datadog credentials Secret

Autopilot uses Datadog's Metrics API and requires a Datadog API key and Application key to authenticate. Create a Kubernetes Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: datadog-autopilot-credentials
  namespace: datadog-ns
  labels:
    app: autopilot
    component: datadog-provider
type: Opaque
data:
  # Base64-encoded Datadog API Key
  api-key: <base64-encoded-api-key>
  # Base64-encoded Datadog Application Key
  app-key: <base64-encoded-app-key>
```

- Replace the namespace, secret name, and encoded key values as required.
- Ensure Autopilot has RBAC permission to read this Secret.
- The `app-key` must have metrics Read permission.

#### Step 2 – Configure the Datadog Agent to export PX metrics

**2.1** Create a Datadog Agent values file (for example, `datadog_config.yaml`):

```yaml
datadog:
  site: "datadoghq.com"
  clusterName: "your-cluster-name"
  apiKeyExistingSecret: "datadog-autopilot-credentials"
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

Use your own `site`, `clusterName`, and `apiKeyExistingSecret`. The Agent scrapes PX metrics and sends them to Datadog.

**2.2** Install the Datadog Agent via Helm:

```shell
helm repo add datadog https://helm.datadoghq.com
helm upgrade --install datadog-agent datadog/datadog -f ./datadog_config.yaml
```

### Configuration

#### Step 2.3 – Annotate PX, Stork, and Autopilot pods

Configure Datadog auto-discovery annotations so the Agent knows which endpoints to scrape. The typical Prometheus-style service endpoints are:

| Component | Endpoint | Metrics filter |
|-----------|----------|----------------|
| Portworx API | `http://%%host%%:17001/metrics` | `px_*` |
| Stork | `http://%%host%%:9091/metrics` | `stork_*` |
| Autopilot | `http://%%host%%:9628/metrics` | `autopilot_*` |

> **Note:** Portworx has many metrics. For most use cases, Portworx API metrics alone are sufficient.

Apply a `ComponentK8sConfig` CR to add the annotations:

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

At this point, the Datadog Agent is configured to scrape PX metrics and the PX, Stork, and Autopilot pods are annotated for auto-discovery.
You can verify the Agent is scraping metrics by running `kubectl exec <datadog-agent-pod> -n datadog-ns -- agent status` and looking for `portworx` in the `Checks` section.

However, Autopilot is not yet configured to use the Datadog provider.

#### Step 3 – Configure the Autopilot Datadog provider in StorageCluster

Enable the Datadog provider in your `StorageCluster` spec under the `autopilot` section:

```yaml
spec:
  autopilot:
    enabled: true
    providers:
    - name: datadog
      type: datadog
      params:
        url: https://datadoghq.com
        secretName: datadog-autopilot-credentials
        secretNamespace: datadog-ns
  monitoring:
    prometheus:
      enabled: false
      exportMetrics: true
```

Key points:
- `type: datadog` tells Autopilot to use the Datadog provider.
- `secretName`/`secretNamespace` must match the Secret created in Step 1.
- Both Datadog and Prometheus are supported simultaneously as well as independently. However, an AutopilotRule configured for one provider cannot interchangeably work with the other.
- If the Datadog Secret is updated, the Autopilot deployment must be restarted.

Apply the updated `StorageCluster` spec and wait for Autopilot to roll out with Datadog support.

To configure Autopilot rules, see the [Autopilot documentation][12].

### Validation

Run the following command to confirm the Agent is scraping PX metrics:

```shell
kubectl exec <datadog-agent-pod> -n <datadog-namespace> -- agent status
```

Look for `openmetrics` instances under the `Checks` section with `portworx`, `stork`, and `autopilot` namespaces.

## Compatibility

This integration is compatible with Portworx 1.4.0 and later versions.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration. For a full reference of all Portworx metrics, see the [Portworx Metrics Reference][13].

### Events

The Portworx integration does not include any events.

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

### Autopilot not using Datadog provider

- Ensure the `datadog-autopilot-credentials` Secret exists in the correct namespace and contains valid base64-encoded keys.
- If the Secret was updated after Autopilot started, restart the Autopilot deployment:
  ```shell
  kubectl rollout restart deployment autopilot -n portworx
  ```

## Further Reading

Additional helpful documentation, links, and articles:

- [Monitoring multi-cloud container storage with Portworx and Datadog][11]


[10]: https://github.com/DataDog/integrations-extras/blob/master/portworx/metadata.csv
[11]: https://www.datadoghq.com/blog/portworx-integration/
[12]: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot
[13]: https://docs.portworx.com/portworx-enterprise/reference/metrics#storage-pool-metrics
