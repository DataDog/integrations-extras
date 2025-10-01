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

1. Install the [developer toolkit][2] on any machine.
2. Run `ddev release build stonebranch` to build the package.
3. [Download the Datadog Agent][3].
4. Upload the build artifact to any host with an Agent and run:
   ```bash
   datadog-agent integration install -w path/to/stonebranch/dist/<ARTIFACT_NAME>.whl
   ```

### Configuration

#### Metric Collection and Log File Setup

1. Edit your `conf.d/stonebranch.yaml` file:

```yaml
init_config:

instances:
  - url: "https://your-uc-server:8080"
    username: "your-username"
    password: "your-password"
    log_path: "/opt/stonebranch/uc/logs/uc.log"  # Optional: specify log path
    verify_ssl: true
    tags:
      - "env:production"
      - "datacenter:us-east-1"

logs:
  - type: file
    path: "/opt/stonebranch/uc/logs/uc.log"
    service: "stonebranch-uc"
    source: "stonebranch"
    tags:
      - "env:production"
      - "component:universal-controller"
    multiline:
      pattern_start: "\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}"
      match_for_start: true
```

2. [Restart the Agent][4].

#### Log Collection Setup

##### Log Parsing

The integration automatically parses UC logs to extract:
- Timestamp
- Log level (INFO, WARN, ERROR, DEBUG)
- Component/module
- Message content
- Job execution details
- Error traces

##### Log Rotation and Permissions

Ensure the Datadog Agent has read permissions on:
- Current log file
- Rotated log files (if log rotation is enabled)

### Validation

Run the [Agent's status subcommand][5] and look for `stonebranch` under the Checks section.

Alternatively, you can test the integration directly:

```bash
sudo -u dd-agent datadog-agent check stonebranch
```

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

See [service_checks.json][8] for a list of service checks provided by this integration.

## Log Collection

### Log Types

The integration categorizes logs into:

- **Application logs**: General UC application events
- **Job logs**: Job execution, status changes, workflow progression
- **Audit logs**: User actions, configuration changes, security events
- **Error logs**: System errors, exceptions, failure details
- **Performance logs**: Resource usage, timing metrics, bottlenecks

### Log Processing

Logs are automatically parsed and enriched with:
- Structured timestamps
- Log levels mapped to Datadog severity
- Component categorization
- Job correlation IDs
- Error stack traces

## Troubleshooting

### Common Issues

1. **Connection failures**: Verify UC server URL and credentials
2. **Log file access**: Check file permissions and path configuration
3. **SSL certificate errors**: Set `verify_ssl: false` for self-signed certificates
4. **Missing metrics**: Ensure UC API endpoints are accessible

### Debug Mode

Enable debug logging by adding to your `datadog.yaml`:

```yaml
log_level: debug
```

Then check the Agent logs for detailed troubleshooting information.

### Getting Help

Need help? Contact [Datadog support][9].

## Further Reading

Additional helpful documentation, links, and articles:

- [Stonebranch Universal Controller Documentation][1]
- [OpenTelemetry Integration Guide][10]
- [Stonebranch Metrics Reference][6]
- [Custom Properties Configuration][7]

[1]: https://www.stonebranch.com/universal-automation-platform/
[2]: https://docs.datadoghq.com/developers/integrations/python/
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://stonebranchdocs.atlassian.net/wiki/spaces/UA78/pages/1086492473/Provided+Metrics
[7]: https://stonebranchdocs.atlassian.net/wiki/spaces/UC78/pages/1086484929/Properties#Properties-Overview
[8]: https://github.com/DataDog/integrations-extras/blob/master/stonebranch/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://stonebranchdocs.atlassian.net/wiki/spaces/UC78/pages/1086463674/Integrating+OpenTelemetry