# Logstash Integration

## Overview

Get metrics from Logstash service in real time to:

- Visualize and monitor Logstash states.
- Be notified about Logstash events.

## Setup

The Logstash check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Logstash check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `logstash` package, run:

   ```shell
   ddev -e release build logstash
   ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_LOGSTASH_ARTIFACT_>/<LOGSTASH_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `logstash.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your Logstash [metrics](#metric-collection) and [logs](#logs-collection). See the [sample logstash.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

#### Metric Collection

Add this configuration setup to your `conf.yaml` file to start gathering your [Logstash metrics][11]:

```yaml
init_config:

instances:
  # The URL where Logstash provides its monitoring API.
  # This will be used to fetch various runtime metrics about Logstash.
  #
  - url: http://localhost:9600
```

Configure it to point to your server and port.

See the [sample conf.yaml][12] for all available configuration options.

Finally, [restart the Agent][13] to begin sending Logstash metrics to Datadog.

#### Log Collection

Datadog has [an output plugin][14] for Logstash that takes care of sending your logs to your Datadog platform.

To install this plugin run the following command:

- `logstash-plugin install logstash-output-datadog_logs`

Then configure the `datadog_logs` plugin with your [Datadog API key][15]:

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

Additional parameters can be used to change the endpoint used in order to go through a [proxy][16]:

- `host`: The proxy endpoint for logs not directly forwarded to Datadog (default value: `http-intake.logs.datadoghq.com`).
- `port`: The proxy port for logs not directly forwarded to Datadog (default value: `80`).
- `ssl_port`: The port used for logs forwarded with a secure TCP/SSL connection to Datadog (default value: `443`).
- `use_ssl`: Instructs the Agent to initialize a secure TCP/SSL connection to Datadog (default value: `true`).
- `no_ssl_validation`: Disables SSL hostname validation (default value: `false`).

This also can be used to send logs to **Datadog EU** by setting:

```conf
output {
   datadog_logs {
       api_key => "<DATADOG_API_KEY>"
       host => "http-intake.logs.datadoghq.eu"
   }
}
```

##### Add metadata to your logs

In order to get the best use out of your logs in Datadog, it is important to have the proper metadata associated with your logs, including hostname and source. By default, the hostname and timestamp should be properly remapped thanks to Datadog's default [remapping for reserved attributes][17]. To make sure the service is correctly remapped, add its attribute value to the service remapping list.

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

This triggers the [integration automatic setup][18] in Datadog.

##### Custom tags

[Host tags][19] are automatically set on your logs if there is a matching hostname in your [infrastructure list][20]. Use the `ddtags` attribute to add custom tags to your logs:

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

[Run the Agent's `status` subcommand][21] and look for `logstash` under the Checks section.

## Compatibility

The Logstash check is compatible with Logstash 5.x, 6.x and 7.x versions. It also supports the new multi-pipelines metrics introduced in Logstash 6.0. Tested with Logstash versions 5.6.15, 6.3.0 and 7.0.0.

## Data Collected

### Metrics

See [metadata.csv][22] for a list of metrics provided by this check.

### Events

The Logstash check does not include any events.

### Service checks

`logstash.can_connect`:

Returns `Critical` if the Agent cannot connect to Logstash to collect metrics; returns `OK` otherwise.

## Troubleshooting

### Agent cannot connect

```text
    logstash
    -------
      - instance #0 [ERROR]: "('Connection aborted.', error(111, 'Connection refused'))"
      - Collected 0 metrics, 0 events & 1 service check
```

Check that the `url` in `conf.yaml` is correct.

If you need further help, contact [Datadog support][23].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/logstash/datadog_checks/logstash/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: #metrics
[12]: https://github.com/DataDog/integrations-extras/blob/master/logstash/datadog_checks/logstash/data/conf.yaml.example
[13]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[14]: https://github.com/DataDog/logstash-output-datadog_logs
[15]: https://app.datadoghq.com/account/settings#api
[16]: https://docs.datadoghq.com/agent/proxy/#proxy-for-logs
[17]: /logs/#edit-reserved-attributes
[18]: /logs/processing/#integration-pipelines
[19]: /getting_started/tagging/assigning_tags
[20]: https://app.datadoghq.com/infrastructure
[21]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[22]: https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv
[23]: http://docs.datadoghq.com/help
