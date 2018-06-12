# Logstash Integration

## Overview

Get metrics from Logstash service in real time to:

* Visualize and monitor Logstash states.
* Be notified about Logstash events.

## Setup

The Logstash check is **NOT** included in the [Datadog Agent](https://app.datadoghq.com/account/settings#agent) package.

### Installation

To install the Logstash check on your host:

1. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).
2. Download the [check.py](https://github.com/DataDog/integrations-extras/blob/master/logstash/check.py) file for Logstash.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `logstash.py`.

### Configuration

To configure the Logstash check: 

1. Create a `logstash.d/` folder in the `conf.d/` folder at the root of your Agent's directory. 
2. Create a `conf.yaml` file in the `logstash.d/` folder previously created.
3. Consult the [sample logstash.yaml](https://github.com/DataDog/integrations-extras/blob/master/logstash/conf.yaml.example) file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml`  to start collecting your [metrics](#metric-collection) or [logs](#log-collection)
5. [Restart the Agent](https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent).

#### Metric Collection

* Add this configuration setup to your `conf.yaml` file to start gathering your [Logstash metrics](#metrics):

```
init_config:

instances:
  #   The URL where Logstash provides its monitoring API. This will be used to fetch various runtime metrics about Logstash.
  #
  - url: http://localhost:9600
```

Configure it to point to your server and port.

See the [sample conf.yaml](https://github.com/DataDog/integrations-extras/blob/master/logstash/conf.yaml.example) for all available configuration options.
* [Restart the Agent](https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent) to begin sending Logstash metrics to Datadog.

#### Log Collection

Follow those [instructions](https://docs.datadoghq.com/logs/log_collection/logstash/) to start forwarding logs to Datadog with Logstash.

## Validation

[Run the Agent's `status` subcommand](https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information) and look for `logstash` under the Checks section.

## Compatibility

The Logstash check is compatible with Logstash 5.6 and possible earlier versions. Currently it does not support the new pipelines metrics in Logstash 6.0 yet.

## Data Collected
### Metrics
See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv) for a list of metrics provided by this check.

### Events
The Logstash check does not include any events at this time.

### Service checks

`logstash.can_connect`:

Returns `Critical` if the Agent cannot connect to Logstash to collect metrics.

## Troubleshooting

### Agent cannot connect
```
    logstash
    -------
      - instance #0 [ERROR]: "('Connection aborted.', error(111, 'Connection refused'))"
      - Collected 0 metrics, 0 events & 1 service check
```

Check that the `url` in `conf.yaml` is correct.

If you need further help, contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog]( https://www.datadoghq.com/blog/)

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/logstash/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://www.datadoghq.com/blog/
[8]: https://docs.datadoghq.com/logs/log_collection/logstash/
