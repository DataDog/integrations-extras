# Akeyless Gateway

## Overview

The Akeyless Platform is a unified secrets management system that enables you to store, protect, rotate, and dynamically create credentials, certificates, and encryption keys. Our platform supports several use cases, including managing static and dynamic credentials, certificate automation, encryption and digital signing, and zero-trust application access that secures remote access to your internal resources.

This integration allows you to visualize and monitor performance of your [Akeyless Gateway][2]. Telemetry metrics are sourced from the application and the runtime environment.

**Note:** Starting with Gateway v5.0.0, the Gateway exposes metrics natively over Prometheus/OpenMetrics instead of shipping them itself through an embedded OpenTelemetry exporter. This changed how the integration is configured: see [Configure](#configure) below for the setup that matches your Gateway version.

## Setup

Akeyless offers a unique Gateway which adds an extra level of protection between your private network and the cloud. Acting as a SaaS extension of our core services, our stateless Gateway enables a transparent internal operation with a robust out-of-the-box mechanism to ensure service continuity and recovery without having to change any network infrastructure in order to work with your internal resources.

To configure the integration with Datadog to view important Akeyless Gateway metrics, follow the instructions below for your Gateway version and deployment method.

### Prerequisites

- An Akeyless Gateway either running or being deployed for the first time.
- **For Gateway v5.0.0 and later:** the [Datadog Agent][8] installed somewhere that can reach the Gateway's metrics endpoint on port `8000` (for example, in the same Kubernetes cluster, or on the same Docker host). The Datadog API key and site are configured on the Agent, not on the Gateway.
- **For Gateway versions prior to 5.0.0 (legacy):** no separate Agent is required. The Gateway ships metrics directly to Datadog using its built-in OpenTelemetry exporter, configured with your Datadog API key and site.

### Configure

This integration works with one Gateway or multiple instances using the same API key. Metrics can be shown per `host` or `instance` in the **Akeyless GW** dashboard.

Configuration differs by Gateway version, since v5.0.0 changed how metrics are exposed. Follow the section that matches your Gateway version below.

#### Gateway v5.0.0 and later

From v5.0.0, the Gateway exposes Prometheus-format metrics natively on port `8000` at the `/metrics` path (metric names such as `akeyless_gw_system_healthcheck_status`, `akeyless_gw_quota_*`, and so on). Datadog is a push-based backend, so it does not scrape this endpoint by itself: the Datadog Agent's [OpenMetrics check][9] (via Autodiscovery) does the scraping and forwards the samples to Datadog. The Datadog API key and site are configured on the Agent, **not** on the Gateway.

**For a Gateway running on Kubernetes**

1. Enable metrics on the Gateway. In your `values.yaml` file for the unified `akeyless-gateway` chart:

    ```yaml
    globalConfig:
      metrics:
        enabled: true
    ```

    (For the legacy `akeyless-api-gateway` chart, the Gateway still serves native `/metrics` on port `8000`; set `ENABLE_METRICS: "true"` as an environment variable instead if it is not already enabled.)

2. Install the [Datadog Agent][8] in your cluster if it is not already running, with your Datadog API key and [Datadog site][1]:

    ```
    helm repo add datadog https://helm.datadoghq.com
    helm repo update

    kubectl create namespace datadog
    kubectl -n datadog create secret generic datadog-secret \
      --from-literal api-key='<Your Datadog API key>'
    ```

    ```yaml
    # datadog-values.yaml
    datadog:
      apiKeyExistingSecret: datadog-secret
      site: <Your Datadog server site>   # e.g. datadoghq.com
      clusterName: <your-cluster-name>
    ```

    ```
    helm install datadog-agent datadog/datadog -n datadog -f datadog-values.yaml
    ```

3. Point the Agent at the Gateway's `/metrics` endpoint using an Autodiscovery annotation on the Gateway pod. The annotation key must match the Gateway container name. Add this to your Gateway `values.yaml`:

    ```yaml
    # Unified chart (akeyless-gateway)
    gateway:
      deployment:
        pod:
          annotations:
            ad.datadoghq.com/akeyless-gateway.checks: |
              {
                "openmetrics": {
                  "instances": [
                    {
                      "openmetrics_endpoint": "http://%%host%%:8000/metrics",
                      "namespace": "akeyless",
                      "metrics": ["akeyless_gw_.*"]
                    }
                  ]
                }
              }
    ```

    ```yaml
    # Legacy chart (akeyless-api-gateway)
    deployment:
      pod:
        annotations:
          ad.datadoghq.com/api-gateway.checks: |
            {
              "openmetrics": {
                "instances": [
                  {
                    "openmetrics_endpoint": "http://%%host%%:8000/metrics",
                    "namespace": "akeyless",
                    "metrics": ["akeyless_gw_.*"]
                  }
                ]
              }
            }
    ```

    If your Gateway serves metrics over HTTPS (Configuration Manager TLS enabled), use `https://%%host%%:8000/metrics` and add `"tls_verify": false` (or configure a proper CA) to the instance.

4. Apply the change:

    ```
    helm upgrade <your-gateway-name> akeyless/akeyless-gateway -f values.yaml
    ```

**For a standalone Gateway running on Docker**

1. Deploy or update your Gateway with metrics enabled, as before:

    ```
    docker run -d -p 8000:8000 -p 8200:8200 -p 18888:18888 -p 8080:8080 -p 8081:8081 -p 5696:5696 -e ENABLE_METRICS="true" --name <your-gateway-name> akeyless/base:latest-akeyless
    ```

    Do **not** mount an `otel-config.yaml` file or set Datadog credentials on the Gateway itself: from v5.0.0, metrics are served natively rather than exported by the Gateway.

2. Install the [Datadog Agent][8] on the same host (or a host that can reach the Gateway on port `8000`), and add an OpenMetrics instance to its configuration (for example in `conf.d/openmetrics.d/conf.yaml`):

    ```yaml
    instances:
      - openmetrics_endpoint: http://<gateway-host>:8000/metrics
        namespace: akeyless
        metrics:
          - akeyless_gw_.*
    ```

    Restart the Agent to pick up the change.

#### Legacy deployments (Gateway versions prior to 5.0.0)

For Gateways older than v5.0.0, keep using the Gateway's built-in OpenTelemetry exporter to ship metrics directly to Datadog, as described below.

**For a Gateway running on Kubernetes**

To configure the Akeyless Gateway integration on a [Gateway running on K8s][3]:

1. In your `values.yaml` file you use to deploy your Gateway on Kubernetes, under the `metrics` section, add the following configuration. Set the relevant API Key of your Datadog server, and the relevant [Datadog site][1] such as: `app.datadoghq.com`.

    ```
    metrics:
      enabled: true  
      config: |
        exporters:    
          datadog:
            api:
              key: "<Your Datadog API key>"
              site: <Your Datadog server site>         
        service:
          pipelines:
            metrics:
              exporters: [datadog]
    ```

2. If you have not yet deployed the Gateway, continue with your installation as usual and run the following command when you are ready to deploy:

    ```
    helm install <your-gateway-name> akeyless/akeyless-api-gateway -f values.yaml
    ```

3. If you are updating an existing Gateway on Kubernetes, run the following commands to update:

    ```
    helm upgrade <your-gateway-name> akeyless/akeyless-api-gateway -f values.yaml
    ```

**For a standalone Gateway running on Docker**

To configure the Akeyless Gateway integration on a [Standalone Gateway][4]:

1. Create a local file called `otel-config.yaml` with the following configuration. Set the relevant API Key of your Datadog server, and the relevant [Datadog site][1] such as `app.datadoghq.com`.

    ```
    exporters:
      datadog:
        api:
          key: "<Your Datadog API key>"
          site: <Your Datadog server site>
    service:
      pipelines:
        metrics:
          exporters: [datadog]
    ```

2. If you have not yet deployed the Gateway, run the following command to spin up your Akeyless Gateway with the `ENABLE_METRICS=true` variable and mount the `otel-config.yaml` file:

    ```
    docker run -d -p 8000:8000 -p 8200:8200 -p 18888:18888 -p 8080:8080 -p 8081:8081 -p 5696:5696 -e ENABLE_METRICS="true" -v $PWD/otel-config.yaml:/akeyless/otel-config.yaml --name <your-gateway-name> akeyless/base:latest-akeyless
    ```

3. If you are updating an existing Gateway, use the same `Admin Access ID` and `Cluster Name` for the updated Gateway in order to retrieve the latest settings and data from the previously removed Docker instance:

    ```
    docker run -d -p 8000:8000 -p 8200:8200 -p 18888:18888 -p 8080:8080 -p 8081:8081 -p 5696:5696 -e ADMIN_ACCESS_ID="p-xxxxxx" -e ADMIN_ACCESS_KEY="62Hu...xxx....qlg=" -e ENABLE_METRICS="true" -v $PWD/otel-config.yaml:/akeyless/otel-config.yaml --name <your-gateway-name> akeyless/base:latest-akeyless
    ```

### Validation

Upon successful setup of the Gateway, go to the [Metrics Explorer][5] on the Datadog site, and filter the Akeyless metrics on the summary page.

- On Gateway v5.0.0 and later, you can also confirm the Agent is scraping correctly with `agent status collector`, and check that its OpenMetrics check for the Gateway shows `[OK]`.
- Metrics from v5.0.0+ deployments appear under the namespace you configured (for example `akeyless.akeyless_gw_*`), while legacy (pre-5.0.0) deployments continue to report under `akeyless.gw.*`.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

**Note on metric names:** the metric prefix depends on your Gateway version and configuration. Gateway versions prior to 5.0.0 report metrics as `akeyless.gw.*` via the built-in OpenTelemetry exporter. Gateway v5.0.0 and later expose metrics natively as `akeyless_gw_*`, which the Datadog Agent's OpenMetrics check reports under `<namespace>.akeyless_gw_*`, where `<namespace>` is the value you set in the Autodiscovery annotation (`akeyless` in the examples above).

**Canonical vs. legacy request counters (v5.0.0+):** `akeyless_gw_system_request_count_total` and `akeyless_gw_system_http_response_status_code_total` are the canonical post-5.0 counters. The non-`_total` names (`akeyless_gw_system_request_count`, `akeyless_gw_system_http_response_status_code`) are transitional legacy names kept for backward compatibility; the `["akeyless_gw_.*"]` filter used above picks up both.

**Gauges despite the `_total` suffix:** `akeyless_gw_system_cpu_throttled_periods_total` and `akeyless_gw_system_cpu_throttled_seconds_total` are emitted as gauges, not counters, even though their names end in `_total`. Do not apply `.as_rate()` (or PromQL `rate()`/`increase()`) to them.

**Metrics that need extra Gateway configuration to populate:**

- `akeyless_gw_system_network_io_receive_bytes` and `akeyless_gw_system_network_io_transmit_bytes` report a flat `0` unless the Gateway environment variable `GW_METRICS_NET_IFACE` is set to the network interface to measure (for example `eth0`). This is most commonly missed on standalone Docker deployments.
- The Gateway's memory limit gauge only appears if `MEM_LIMIT` is set as a plain byte count. A suffixed value such as `512Mi` is silently rejected.

### Service Checks

The Akeyless Gateway integration does not include any service checks.

### Events

The Akeyless Gateway integration does not include any events.

## Support

Need help? Contact [Akeyless Support][7].


[1]: https://docs.datadoghq.com/getting_started/site/
[2]: https://docs.akeyless.io/docs/api-gw
[3]: https://docs.akeyless.io/docs/gateway-k8s
[4]: https://docs.akeyless.io/docs/install-and-configure-the-gateway
[5]: /metric/explorer
[6]: https://github.com/DataDog/integrations-extras/blob/master/akeyless_gateway/metadata.csv
[7]: mailto:support@akeyless.io
[8]: https://docs.datadoghq.com/containers/kubernetes/installation/
[9]: https://docs.datadoghq.com/integrations/openmetrics/
