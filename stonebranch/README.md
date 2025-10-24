# Agent Check: Stonebranch Universal Controller

## Overview

This check monitors [Stonebranch Universal Controller][1] through both metric collection and log parsing.

The Stonebranch Universal Controller integration provides comprehensive monitoring capabilities:

- **Metric Collection**: Collect performance and operational metrics directly from the Universal Controller API
- **Advanced Dashboards**: Create detailed monitoring dashboards to visualize job execution, system performance, and resource utilization
- **Alerting**: Set up proactive alerts for critical workflows, failed jobs, and system issues
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
```

2. [Restart the Agent][4].

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
- Stonebranch metrics (OMS Status, Late-start tasks)

For a complete list of collected metrics including labels, visit our [Metrics Documentation][6]. Custom labels can be enabled for more detailed metric analysis - see [here][7] for configuration details.

### Events

The Stonebranch integration does not include any events.

## Troubleshooting

### Common Issues

1. **Connection failures**: Verify UC server URL and credentials
2. **Missing metrics**: Ensure UC API endpoints are accessible and the user accessing them has, at least "ops_service" permissions.

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