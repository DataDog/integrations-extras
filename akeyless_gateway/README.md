# Akeyless Gateway

## Overview

This integration allows you to visualize and monitor performance of your [Akeyless Gateway][1]. The Telemetry Metrics are based on time series telemetry data metrics from the application and the runtime environment, storing them in a unique database or index, and analyzing data trends over time.

## Setup

**Prerequisites**
- An Akeyless Gateway either running or being deployed for the first time
- Gateway [Auth Method](https://docs.akeyless.io/docs/advance-gw-docker-configuration#authentication) with permissions to create and manage Secrets & Keys and Targets

### Configure

**For a Standalone Gateway Running on Docker**

To configure the Akeyless Gateway integration on a [Standalone Gateway](https://docs.akeyless.io/docs/install-and-configure-the-gateway):

1. Create a local file called `otel-config.yaml` with the below configuration. Set the relevant API Key of your Datadog server, and the relevant site. If your Datadog server is running in the EU site, use `datadoghq.eu`. Default is `datadoghq.us`.

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

2. Run the below command to spin up your Akeyless Gateway with the `ENABLE_METRICS=true` variable and mounting the `otel-config.yaml` file. If you are updating an existing Gateway, use the same `Admin Access ID` and `Cluster Name` for the updated Gateway in order to retrieve the latest settings and data from the previously removed Docker instance.

```
docker run -d -p 8000:8000 -p 8200:8200 -p 18888:18888 -p 8080:8080 -p 8081:8081 -p 5696:5696 -e ENABLE_METRICS="true" -v $PWD/otel-config.yaml:/akeyless/otel-config.yaml  --name <your-gateway-name> akeyless/base:latest-akeyless
```

**For a Gateway Running on Kubernetes**

To configure the Akeyless Gateway integration on a [Gateway on K8s](https://docs.akeyless.io/docs/gateway-k8s):

1. In your `values.yaml` file you use to deploy your Gateway on Kubernetes, under the `metrics` section, add the below configuration. Set the relevant API Key of your Datadog server, and the relevant site. If your Datadog server is running in the EU site, use `datadoghq.eu`. Default is `datadoghq.us`.

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

2. Continue with your Gateway on Kubernetes Installation as usual.

If you are updating an existing Gateway on Kubernetes, run the following commands to update:

```
helm repo update
helm upgrade <your-gateway-name> akeyless/akeyless-api-gateway -f values.yaml
```

### Validation

Upon successful setup of the Gateway, go to the Metrics page on the Datadog platform, and filter the Akeyless metrics on the summary page.

## Data Collected

### Metrics

See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/akeyless_gateway/metadata.csv) for a list of metrics provided by this integration.

### Service Checks

Akeyless Gateway does not include any service checks.

### Events

Akeyless Gateway does not include any events.

## Troubleshooting

Need help? Contact [Akeyless Support][mailto:support@akeyless.io].
