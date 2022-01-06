# Contrast Security Integration

## Overview

The Datadog-Contrast integration allows you to get your Contrast logs into Datadog.

## Setup

### Log collection

Enable logs collection for Datadog Agent in `/etc/datadog-agent/datadog.yaml` on Linux platforms. On other platforms, see the [Agent Configuration Files guide][1] for the location of your configuration file:

```yaml
logs_enabled: true
```

- Add this configuration block to your `contrastsecurity.d/conf.yaml` file to start collecting your Contrast Logs:
- Create a new `conf.yaml` file.
- Add a custom log collection configuration group.

    ```yaml
    logs:
      - type: file
        path: /path/to/contrast/security.log
        service: contrast
        source: contrastsecurity
    ```

For more information on logs, see the [Contrast Security documentation][2].

- [Restart the Datadog Agent][3].

For more information, see the:
- [Datadog Logs documentation][4]
- [Datadog Dashboards API][5]

## Data Collected

### Metrics

The Contrast integration does not include any metrics.

### Events

The Contrast integration does not send any events.

### Service Checks

The Contrast integration does not include any service checks.


[1]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/
[2]: https://docs.contrastsecurity.com/
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/#restart-the-agent
[4]: https://docs.datadoghq.com/logs/log_collection/
[5]: https://docs.datadoghq.com/api/#create-a-dashboard
