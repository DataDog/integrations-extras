# Agent Check: Stonebranch Universal Controller

## Overview

This check monitors [Stonebranch Universal Controller][1] through both metric collection and log parsing.

The Stonebranch Universal Controller integration provides comprehensive monitoring capabilities:

- **Metric Collection**: Collect performance and operational metrics directly from the Universal Controller API
- **Advanced Dashboards**: Create detailed monitoring dashboards to visualize job execution, system performance, and resource utilization
- **Alerting**: Set up proactive alerts for critical workflows, failed jobs, and system issues
- **Log Analysis**: Parse and analyze Universal Controller logs for troubleshooting and audit purposes
- **Workflow Monitoring**: Monitor your automated workflows for errors and gain complete visibility into your most important tasks

## Setup

### Installation

To install the Stonebranch check on your host:

1. [Download the Datadog Agent][3].
2. Install the Stonebranch Integration
3. Configure the yaml with your Universal Controller url and log path.

### Configuration

#### Metric Collection and Log File Setup

1. Edit your `conf.d/stonebranch.yaml` file:

```yaml
init_config:

instances:
  - url: "http://localhost:8080/uc"
    username: "your-username" #user with valid access rights to /resources/metric
    password: "your-password" 

logs:
  - type: file
    path: "/path/to/uc.log" #Path to your Tomcat UC logs.
    service: "stonebranch-uc"
    source: "stonebranch"
    multiline:
      pattern_start: "\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}"
      match_for_start: true
```
Ensure the Datadog Agent has read permissions on:
- Current log file
- Rotated log files (if log rotation is enabled)

2. [Restart the Agent][4].

## Data Collected

### Metrics

The integration collects various metrics from the Universal Controller including:

- Job execution metrics (success/failure rates, execution times)
- System performance metrics (CPU, memory, disk usage)
- Queue metrics (job queue depth, processing rates)
- Connection metrics (database connections, API response times)

For a complete list of collected metrics including labels, visit our [Metrics Documentation][6]. Custom labels can be enabled for more detailed metric analysis - see [here][7] for configuration details.

### Events

The Stonebranch integration does not include any events.

### Service Checks

The Stonebranch integration does not include any service checks.

## Log Collection

The Stonebranch integration collects the log file and its content from the tomcat uc.log.

## Troubleshooting

### Common Issues

1. **Connection failures**: Verify UC server URL and credentials
2. **Log file access**: Check file permissions and path configuration
3. **Missing metrics**: Ensure UC API endpoints are accessible

### Getting Help

Need help? Contact [Datadog support][9].

## Further Reading

Additional helpful documentation, links, and articles:

- [Stonebranch Universal Controller Documentation][1]
- [OpenTelemetry Integration Guide][10]
- [Stonebranch Metrics Reference][6]
- [Custom Properties Configuration][7]

[1]: https://stonebranchdocs.atlassian.net/wiki/spaces/SD/overview
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://stonebranchdocs.atlassian.net/wiki/spaces/UA78/pages/1086492473/Provided+Metrics
[7]: https://stonebranchdocs.atlassian.net/wiki/spaces/UC78/pages/1086484929/Properties#Properties-Overview
[8]: https://github.com/DataDog/integrations-extras/blob/master/stonebranch/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://stonebranchdocs.atlassian.net/wiki/spaces/UC78/pages/1086463674/Integrating+OpenTelemetry