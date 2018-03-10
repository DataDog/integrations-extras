# Logstash Integration

## Overview

Get metrics from Logstash service in real time to:

* Visualize and monitor Logstash states.
* Be notified about Logstash events.

## Setup

### Configuration

Create a file `logstash.yaml` in the Agent's `conf.d` directory.

#### Metric Collection

* Add this configuration setup to your `logstash.yaml` file to start gathering your [Logstash metrics](#metrics):

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

[Run the Agent's `info` subcommand](https://docs.datadoghq.com/agent/faq/agent-status-and-information/), you should see something like the following:

    Checks
    ======

      logstash 
      -----------------
        - instance #0 [OK]
        - Collected 61 metrics, 0 events & 1 service check

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
