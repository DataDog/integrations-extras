# Stonebranch

## Overview
To learn more about this integration, visit https://docs.datadoghq.com/integrations/stonebranch/ 

## Setup

The Stonebranch integration follows through the Stonebranch Datadog extension, which will be installed onto your Datadog Agent. The extension interacts with Stonebranch's Universal Controller API to gather information metrics on the system and report them to Datadog.

### Prerequisites

Have a running Universal Controller instance, which has the Opentelemetry function enabled. (This is enabled by default in the uc.properties)

You need to have a user that has access to the metrics endpoint on your Universal Controller.

Install the Stonebranch Datadog Extension

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