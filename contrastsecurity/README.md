# Contrast Security Integration

## Overview

The Datadog-Constant integration allows you to get your Contrast logs into Datadog.

## Setup

### Set up Contrast Protect logs collection

Enable logs collection for Datadog Agent in `/etc/datadog-agent/datadog.yaml` on Linux platforms. On other platforms, refer to the [Agent Configuration Files guide](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6) for the location of your configuration file:
```
logs_enabled: true
```

* Add this configuration block to your `contrastsecurity.d/conf.yaml` file to start collecting your Contrast Logs:
* Create a new `conf.yaml` file.
* Add a custom log collection configuration group.
```
logs:
  - type: file
    path: /path/to/contrast/security.log
    service: contrast
    source: contrastsecurity
```
For more information on logs: https://docs.contrastsecurity.com/installation-setupconfig.html#log

* [Restart the Datadog Agent](https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#restart-the-agent).

For more information, consult the [Logs Collection documentation](https://docs.datadoghq.com/logs/log_collection/?tab=tailexistingfiles#getting-started-with-the-agent).

For more information, refer to the [Datadog API documentation for creating a dashboard](https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard).

## Data Collected

### Metrics

The Contrast integration does not include any metrics.

### Events

The Contrast integration does not send any events.

### Service Checks

The Contrast integration does not include any service checks.
