# Logstash Integration

## Overview

Get metrics from Logstash service in real time to:

* Visualize and monitor Logstash states.
* Be notified about Logstash events.

## Setup

The Logstash check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Logstash check on your host:

1. [Download the Datadog Agent][2].
2. Download the [`check.py` file][15] for Logstash.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `logstash.py`.

### Configuration

To configure the Logstash check:

1. Create a `logstash.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `logstash.d/` folder previously created.
3. Consult the [sample logstash.yaml][3] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml`  to start collecting your [metrics][5] or [logs][6]
5. [Restart the Agent][7].

#### Metric Collection

* Add this configuration setup to your `conf.yaml` file to start gathering your [Logstash metrics][8]:

```
init_config:

instances:
  #   The URL where Logstash provides its monitoring API. This will be used to fetch various runtime metrics about Logstash.
  #
  - url: http://localhost:9600
```

Configure it to point to your server and port.

See the [sample conf.yaml][3] for all available configuration options.
* [Restart the Agent][7] to begin sending Logstash metrics to Datadog.

#### Log Collection

Datadog has [an ouput plugin][16] for Logstash that takes care of sending your logs to your Datadog platform.

To install this plugin run the following command:

* `logstash-plugin install logstash-output-datadog_logs`

Then configure the `datadog_logs` plugin with your [Datadog API key][21]:

```
output {
    datadog_logs {
        api_key => "<DATADOG_API_KEY>"
    }
}
```

Additional parameters can be used to change the endpoint used in order to go through a proxy:

* host: Proxy endpoint when logs are not directly forwarded to Datadog (default value is `intake.logs.datadoghq.com`)
* port: Proxy port when logs are not directly forwarded to Datadog	 (default value is `10516`)
* use_ssl: If true, the agent initializes a secure connection to Datadog. In clear TCP otherwise. (default value is `true`)

 This also can be used to send logs to **Datadog EU** by setting:

 ```
output {
    datadog_logs {
        api_key => "<DATADOG_API_KEY>"
        host => "tcp-intake.logs.datadogh.eu
        port => "443"
    }
}
```

##### Add metadata to your logs

In order to get the best use out of your logs in Datadog, it is important to have the proper metadata associated with your logs (including hostname and source). By default, the hostname and timestamp should be properly remapped thanks to our default [remapping for reserved attributes][17]. To make sure the service is correctly remapped, add its attribute value to the Service remapping list.

##### Source

Setup a Logstash filter to set the source (Datadog integration name) on your logs. 

```
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

[Host tags][20] are automatically set on your logs if there is a matching hostname in your [infrastructure list][19]. Use the `ddtags` attribute to add custom tags to your logs:

```
filter {
  mutate {
    add_field => {
        "ddtags" => "env:test,<KEY:VALUE>"
       }
    }
 }
```


### Validation

[Run the Agent's `status` subcommand][12] and look for `logstash` under the Checks section.

## Compatibility

The Logstash check is compatible with Logstash 5.6 and possible earlier versions. Currently it does not support the new pipelines metrics in Logstash 6.0 yet.

## Data Collected
### Metrics
See [metadata.csv][13] for a list of metrics provided by this check.

### Events
The Logstash check does not include any events.

### Service checks

`logstash.can_connect`:

Returns `Critical` if the Agent cannot connect to Logstash to collect metrics, returns `OK` otherwise.

## Troubleshooting

### Agent cannot connect
```
    logstash
    -------
      - instance #0 [ERROR]: "('Connection aborted.', error(111, 'Connection refused'))"
      - Collected 0 metrics, 0 events & 1 service check
```

Check that the `url` in `conf.yaml` is correct.

If you need further help, contact [Datadog support][14].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://github.com/DataDog/integrations-extras/blob/master/logstash/conf.yaml.example
[5]: #metric-collection
[6]: #log-collection
[7]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[8]: #metrics
[12]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[13]: https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv
[14]: http://docs.datadoghq.com/help/
[15]: https://github.com/DataDog/integrations-extras/blob/master/logstash/check.py
[16]: https://github.com/DataDog/logstash-output-datadog_logs
[17]: /logs/#edit-reserved-attributes
[18]: /logs/processing/#integration-pipelines
[19]: https://app.datadoghq.com/infrastructure
[20]: /getting_started/tagging/assigning_tags/
[21]: https://app.datadoghq.com/account/settings#api
[22]: https://docs.datadoghq.com/agent/proxy/?tab=agentv6#proxy-for-logs
