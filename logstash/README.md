# Logstash Integration

## Overview

Get metrics from logstash service in real time to:

* Visualize and monitor logstash states
* Be notified about logstash events.

## Installation

Install the `dd-check-logstash` package manually or with your favorite configuration manager

## Configuration

Edit the `logstash.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

      logstash 
      -----------------
        - instance #0 [OK]
        - Collected 61 metrics, 0 events & 1 service check

## Compatibility

The logstash check is compatible with Logstash 5.6 and possible earlier versions. Currently it does not support the new pipelines metrics in Logstash 6.0 yet.

## Metrics

See [metadata.csv](metadata.csv) for a list of metrics provided by this integration.

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
