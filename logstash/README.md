# Logstash Integration

## Overview

Get metrics from Logstash in real time to:

- Visualize and monitor Logstash states.
- Be notified about Logstash events.

## Setup

### Installation

The Logstash check is not included in the [Datadog Agent][1] package, so you need to install it.

<!-- xxx tabs xxx -->
<!-- xxx tab "Host" xxx -->

#### Host

For Agent v7.21+ / v6.21+, follow the instructions below to install the Logstash check on your host. For earlier versions of the Agent, see [Use Community Integrations][2]. 

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-logstash==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][3].

<!-- xxz tab xxx -->
<!-- xxx tab "Containerized" xxx -->

#### Containerized

Use the following Dockerfile to build a custom Datadog Agent image that includes the Logstash integration.

```dockerfile
FROM gcr.io/datadoghq/agent:latest
RUN datadog-agent integration install -r -t datadog-logstash==<INTEGRATION_VERSION>
```

If you are using Kubernetes, update your Datadog Operator or Helm chart configuration to pull this custom Datadog Agent image.

See [Use Community Integrations][2] for more context.

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Configuration

#### Metric collection

<!-- xxx tabs xxx -->
<!-- xxx tab "Host" xxx -->

##### Host

1. Edit the `logstash.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][4].

   ```yaml
   init_config:

   instances:
     # The URL where Logstash provides its monitoring API.
     # This will be used to fetch various runtime metrics about Logstash.
     #
     - url: http://localhost:9600
   ```

   See the [sample logstash.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

<!-- xxz tab xxx -->
<!-- xxx tab "Containerized" xxx -->

##### Containerized

For containerized environments, use an Autodiscovery template with the following parameters:

| Parameter            | Value                                |
| -------------------- | ------------------------------------ |
| `<INTEGRATION_NAME>` | `logstash`                           |
| `<INIT_CONFIG>`      | blank or `{}`                        |
| `<INSTANCE_CONFIG>`  | `{"server": "http://%%host%%:9600"}` |

To learn how to apply this template, see [Docker Integrations][7] or [Kubernetes Integrations][8].

See the [sample logstash.d/conf.yaml][5] for all available configuration options.

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

#### Log collection

Datadog has [an output plugin][13] for Logstash that takes care of sending your logs to your Datadog platform.

To install this plugin run the following command:

- `logstash-plugin install logstash-output-datadog_logs`

Then configure the `datadog_logs` plugin with your [Datadog API key][14]:

```conf
output {
    datadog_logs {
        api_key => "<DATADOG_API_KEY>"
    }
}
```

By default, the plugin is configured to send logs through HTTPS (port 443) using gzip compression.
You can change this behavior by using the following parameters:

- `use_http`: Set this to `false` if you want to use TCP forwarding and update the `host` and `port` accordingly (default is `true`).
- `use_compression`: Compression is only available for HTTP. Disable it by setting this to `false` (default is `true`).
- `compression_level`: Set the compression level from HTTP. The range is from 1 to 9, 9 being the best ratio (default is `6`).

Additional parameters can be used to change the endpoint used in order to go through a [proxy][15]:

- `host`: The proxy endpoint for logs not directly forwarded to Datadog (default value: `http-intake.logs.datadoghq.com`).
- `port`: The proxy port for logs not directly forwarded to Datadog (default value: `80`).
- `ssl_port`: The port used for logs forwarded with a secure TCP/SSL connection to Datadog (default value: `443`).
- `use_ssl`: Instructs the Agent to initialize a secure TCP/SSL connection to Datadog (default value: `true`).
- `no_ssl_validation`: Disables SSL hostname validation (default value: `false`).

**Note**: Set `host` and `port` to your region {{< region-param key="http_endpoint" code="true" >}} {{< region-param key="http_port" code="true" >}}.

```conf
output {
   datadog_logs {
       api_key => "<DATADOG_API_KEY>"
       host => "http-intake.logs.datadoghq.eu"
   }
}
```

##### Add metadata to your logs

To get the best use out of your logs in Datadog, it is important to have the proper metadata associated with your logs, including hostname and source. By default, the hostname and timestamp should be properly remapped thanks to Datadog's default [remapping for reserved attributes][16]. To make sure the service is correctly remapped, add its attribute value to the service remapping list.

##### Source

Set up a Logstash filter to set the source (Datadog integration name) on your logs.

```conf
filter {
  mutate {
    add_field => {
 "ddsource" => "<MY_SOURCE_VALUE>"
       }
    }
 }
```

This triggers the [integration automatic setup][17] in Datadog.

##### Custom tags

[Host tags][18] are automatically set on your logs if there is a matching hostname in your [infrastructure list][19]. Use the `ddtags` attribute to add custom tags to your logs:

```conf
filter {
  mutate {
    add_field => {
        "ddtags" => "env:test,<KEY:VALUE>"
       }
    }
 }
```

### Validation

[Run the Agent's `status` subcommand][20] and look for `logstash` under the Checks section.

## Compatibility

The Logstash check is compatible with Logstash 5.x, 6.x and 7.x versions. It also supports the new multi-pipelines metrics introduced in Logstash 6.0. Tested with Logstash versions 5.6.15, 6.3.0 and 7.0.0.

## Data Collected

### Metrics

See [metadata.csv][21] for a list of metrics provided by this check.

### Events

The Logstash check does not include any events.

### Service Checks

See [service_checks.json][23] for a list of service checks provided by this integration.

## Troubleshooting

### Agent cannot connect

```text
    logstash
    -------
      - instance #0 [ERROR]: "('Connection aborted.', error(111, 'Connection refused'))"
      - Collected 0 metrics, 0 events & 1 service check
```

Check that the `url` in `conf.yaml` is correct.

If you need further help, contact [Datadog support][22].

[1]: https://app.datadoghq.com/account/settings/agent/latest
[2]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[3]: https://docs.datadoghq.com/getting_started/integrations/
[4]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[5]: https://github.com/DataDog/integrations-extras/blob/master/logstash/datadog_checks/logstash/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/containers/docker/integrations
[8]: https://docs.datadoghq.com/containers/kubernetes/integrations/
[13]: https://github.com/DataDog/logstash-output-datadog_logs
[14]: https://app.datadoghq.com/organization-settings/api-keys
[15]: https://docs.datadoghq.com/agent/proxy/#proxy-for-logs
[16]: https://docs.datadoghq.com/logs/#edit-reserved-attributes
[17]: https://docs.datadoghq.com/logs/processing/#integration-pipelines
[18]: https://docs.datadoghq.com/getting_started/tagging/assigning_tags
[19]: https://app.datadoghq.com/infrastructure
[20]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[21]: https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv
[22]: http://docs.datadoghq.com/help
[23]: https://github.com/DataDog/integrations-extras/blob/master/logstash/assets/service_checks.json