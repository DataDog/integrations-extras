# Logstash Integration

## Overview

Get metrics from Logstash service in real time to:

- Visualize and monitor Logstash states.
- Be notified about Logstash events.

## Setup

The Logstash check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Logstash check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-logstash==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `logstash.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Logstash [metrics](#metric-collection) and [logs](#log-collection). See the [sample logstash.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

#### Metric collection

Add this configuration setup to your `conf.yaml` file to start gathering your [Logstash metrics][10]:

```yaml
init_config:

instances:
  # The URL where Logstash provides its monitoring API.
  # This will be used to fetch various runtime metrics about Logstash.
  #
  - url: http://localhost:9600
```

Configure it to point to your server and port.

See the [sample conf.yaml][11] for all available configuration options.

Finally, [restart the Agent][12] to begin sending Logstash metrics to Datadog.

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

In order to get the best use out of your logs in Datadog, it is important to have the proper metadata associated with your logs, including hostname and source. By default, the hostname and timestamp should be properly remapped thanks to Datadog's default [remapping for reserved attributes][16]. To make sure the service is correctly remapped, add its attribute value to the service remapping list.

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


[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/logstash/datadog_checks/logstash/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: #metrics
[11]: https://github.com/DataDog/integrations-extras/blob/master/logstash/datadog_checks/logstash/data/conf.yaml.example
[12]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[13]: https://github.com/DataDog/logstash-output-datadog_logs
[14]: https://app.datadoghq.com/account/settings#api
[15]: https://docs.datadoghq.com/agent/proxy/#proxy-for-logs
[16]: /logs/#edit-reserved-attributes
[17]: /logs/processing/#integration-pipelines
[18]: /getting_started/tagging/assigning_tags
[19]: https://app.datadoghq.com/infrastructure
[20]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[21]: https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv
[22]: http://docs.datadoghq.com/help
[23]: https://github.com/DataDog/integrations-extras/blob/master/logstash/assets/service_checks.json
