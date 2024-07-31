# CloudQuery

![datadog-integration][1]

## Overview

[CloudQuery][2] is an [open-source][3], high-performance data integration framework built for developers, with support for a wide range of plugins.

CloudQuery extracts, transforms, and loads configuration from cloud APIs to a variety of supported destinations such as databases, data lakes, or streaming platforms for further analysis.

## Setup

### Installation

To ingest OpenTelemetry traces, metrics, and logs from CloudQuery, install the [Datadog Agent][11] version >=6.48.0 or >=7.48.0.
Alternatively, you can use OpenTelemetry Collector and Datadog Exporter as described below.

### Configuration

CloudQuery supports [OpenTelemetry][5] traces, metrics, and logs out of the box.
There are multiple ways to configure OpenTelemetry with Datadog:

- [Using an OpenTelemetry collector](#opentelemetry-collector)
- [Direct OTEL Ingestion by the Datadog Agent through a configuration file](#datadog-agent-otel-ingestion-through-a-configuration-file)
- [Direct OTEL ingestion by the Datadog Agent through environment variables](#datadog-agent-otel-ingestion-through-environment-variables)

For more information, see [OpenTelemetry in Datadog][6].

#### OpenTelemetry collector

To configure an OpenTelemetry collector with Datadog:

1. Create a configuration file. For example, create an `otel_collector_config.yaml` file with the content below:

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"

processors:
  batch/datadog:
    send_batch_max_size: 1000
    send_batch_size: 100
    timeout: 10s

exporters:
  datadog:
    api:
      site: ${env:DATADOG_SITE}
      key: ${env:DATADOG_API_KEY}

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch/datadog]
      exporters: [datadog]
    traces:
      receivers: [otlp]
      processors: [batch/datadog]
      exporters: [datadog]
    logs:
      receivers: [otlp]
      processors: [batch/datadog]
      exporters: [datadog]
```

2. Run the collector with the following command (replace `DATADOG_SITE` and `DATADOG_API_KEY` with your own values):

```bash
docker run \
    -p 4318:4318 \
    -e DATADOG_SITE=$DATADOG_SITE \
    -e DATADOG_API_KEY=$DATADOG_API_KEY \
    --hostname $(hostname) \
    -v $(pwd)/otel_collector_config.yaml:/etc/otelcol-contrib/config.yaml \
    otel/opentelemetry-collector-contrib:0.104.0
```

For additional ways to run the collector, see [OpenTelemetry Deployment][7].

#### Datadog Agent OTEL ingestion through a configuration file

1. Locate your [`datadog.yaml` Agent configuration file][8] and add the following configuration:

```yaml
otlp_config:
  receiver:
    protocols:
      http:
        endpoint: 0.0.0.0:4318
  logs:
    enabled: true
logs_enabled: true
```

2. [Restart][9] the Datadog agent for the change to take effect.

#### Datadog Agent OTEL ingestion through environment variables

1. Pass the `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT` environment variable to the Datadog Agent with a value of `0.0.0.0:4318`.
If you're using Docker compose, see the example below:

```yaml
version: "3.0"
services:
  agent:
    image: gcr.io/datadoghq/agent:7
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
    environment:
      DD_API_KEY: redacted
      DD_SITE: "datadoghq.eu"
      DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT: "0.0.0.0:4318"
      DD_LOGS_ENABLED: "true"
      DD_OTLP_CONFIG_LOGS_ENABLED: "true"
    ports:
      - "4318:4318"
```

2. [Restart][9] the Datadog agent for the change to take effect.

For more ways to configure the Datadog Agent, see [OTLP Ingestion by the Datadog Agent][10].

After you have the Agent or collector ready, specify the endpoint in the source spec:

```yaml
kind: source
spec:
  name: "aws"
  path: "cloudquery/aws"
  registry: "cloudquery"
  version: "VERSION_SOURCE_AWS"
  tables: ["aws_s3_buckets"]
  destinations: ["postgresql"]
  otel_endpoint: "0.0.0.0:4318"
  otel_endpoint_insecure: true
  spec:
```

### Validation

Run `cloudquery sync spec.yml`.
After ingestion starts, you should start seeing the traces in the Datadog [**APM Traces Explorer**][12].
You can also validate metrics and logs in the [**Metrics Summary**][13] and [**Log Explorer**][14].

## Data Collected

### Metrics

The CloudQuery does not include any metrics.

### Service Checks

The CloudQuery does not include any service checks.

### Events

The CloudQuery does not include any events.

## Uninstallation

If you use the OpenTelemetry collector, you can stop it by running `docker stop <container_id>`.
If you use the Datadog Agent, remove the configuration or environment variables you added and [restart][9] the agent.
Finally, delete the dashboard from your Datadog account.

## Support

For support, contact [CloudQuery][4].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/cloudquery/images/cloudquery_logo_png_dark_background.png
[2]: https://www.cloudquery.io/
[3]: https://github.com/cloudquery/cloudquery
[4]: https://www.cloudquery.io/pricing
[5]: https://opentelemetry.io/
[6]: https://docs.datadoghq.com/opentelemetry/
[7]: https://docs.datadoghq.com/opentelemetry/collector_exporter/deployment#running-the-collector
[8]: https://docs.datadoghq.com/agent/configuration/agent-configuration-files/
[9]: https://docs.datadoghq.com/agent/configuration/agent-commands/#restart-the-agent
[10]: https://docs.datadoghq.com/opentelemetry/interoperability/otlp_ingest_in_the_agent#enabling-otlp-ingestion-on-the-datadog-agent
[11]: https://docs.datadoghq.com/agent/
[12]: https://app.datadoghq.com/apm/traces
[13]: https://app.datadoghq.com/metric/summary
[14]: https://app.datadoghq.com/logs
