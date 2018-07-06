# Portworx Integration

## Overview

Get metrics from Portworx service in real time to:

- Monitor health and performance of your Portworx Cluster
- Track disk usage, latency and throughput for Portworx volumes

## Setup

### Installation

The Portworx check is included in the [Datadog Agent][1] package, so you don't need to install anything else on your Portworx servers.

### Configuration

Create a file `portworx.yaml` in the Agent's `conf.d` directory.

#### Metric Collection

- Add this configuration setup to your `portworx.yaml` file to start gathering your [portworx metrics][2]:

```
init_config:

instances:
 # url of the metrics endpoint of prometheus
 - prometheus_endpoint: http://localhost:9001/metrics
```

Configure it to point to your server and port.

See the [sample portworx.yaml][3](https://github.com/DataDog/integrations-extras/blob/master/portworx/conf.yaml.example) for all available configuration options.

- [Restart the Agent][4](https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent) to begin sending Portworx metrics to Datadog.

### Validation

[Run the Agent's `info` subcommand][5](https://docs.datadoghq.com/agent/faq/agent-status-and-information/), you should see something like the following:

    Checks
    ======

      portworx
      -----------------
        - instance #0 [OK]
        - Collected 60 metrics, 0 events & 0 service check

## Compatibility

The Portworx check is compatible with Portworx 1.4.0 and possible earlier versions.

## Data Collected

### Metrics

See [metadata.csv][6](https://github.com/DataDog/integrations-extras/blob/master/portworx/metadata.csv) for a list of metrics provided by this integration.

### Events

The Portworx check does not include any events at this time.

## Troubleshooting

### Agent cannot connect

```
    portworx
    -------
      - instance #0 [ERROR]: "('Connection aborted.', error(111, 'Connection refused'))"
      - Collected 0 metrics, 0 events & 0 service check
```

Check that the `url` in `portworx.yaml` is correct.
