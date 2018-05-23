# Logstash Integration

## Overview

Get metrics from Logstash service in real time to:

* Visualize and monitor Logstash states.
* Be notified about Logstash events.

## Setup

### Configuration

Download the [`check.py`](https://github.com/DataDog/integrations-extras/blob/master/logstash/check.py) file, place it in the Agent's `checks.d` directory, and rename it to `logstash.py`. 

Create a file `logstash.yaml` in the Agent's `conf.d` directory.

#### Metric Collection

* Add this configuration setup to your `logstash.yaml` file to start gathering your Logstash metrics:

```
init_config:

instances:
  #   The URL where Logstash provides its monitoring API. This will be used to fetch various runtime metrics about Logstash.
  #
  - url: http://localhost:9600
```

Configure it to point to your server and port.

See the [sample logstash.yaml](https://github.com/DataDog/integrations-extras/blob/master/logstash/conf.yaml.example) for all available configuration options.
* [Restart the Agent](https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent) to begin sending Logstash metrics to Datadog.

#### Log Collection

Follow those [instructions](https://docs.datadoghq.com/logs/faq/how-to-send-logs-to-datadog-via-external-log-shippers/#logstash) to start forwarding logs to Datadog with Logstash.

### Validation

[Run the Agent's `status` subcommand](https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information) and look for `logstash` under the Checks section.

## Compatibility

The Logstash check is compatible with Logstash 5.6 and possible earlier versions. Currently it does not support the new pipelines metrics in Logstash 6.0 yet.

## Data Collected
### Metrics
See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv) for a list of metrics provided by this integration.

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

Check that the `url` in `logstash.yaml` is correct.

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).


[1]: https://github.com/DataDog/integrations-extras/blob/master/logstash/conf.yaml.example
[2]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[3]: https://docs.datadoghq.com/logs/faq/how-to-send-logs-to-datadog-via-external-log-shippers/#logstash
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/logstash/metadata.csv
[6]: https://www.datadoghq.com/blog/
[7]: https://github.com/DataDog/integrations-extras/blob/master/logstash/check.py
