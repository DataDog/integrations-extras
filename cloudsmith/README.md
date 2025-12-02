# Agent Check: Cloudsmith

## Overview

Cloudsmith is a fully managed cloud-native package management platform, used to securely store, manage, and distribute software artifacts for DevOps teams. It supports all major formats including Docker, npm, Maven, Python, RubyGems, and more, with enterprise-grade access control, policy enforcement, and auditing.

This integration enhances visibility into your Cloudsmith organization by collecting real-time observability data and surfacing it within the Datadog platform. Teams can monitor resource usage, enforce security compliance, and audit user activity-directly from within Datadog dashboards and monitors.

The integration collects data from Cloudsmith's APIs and maps them to the following Datadog telemetry types:
- **Metrics**: Storage and bandwidth usage, token activity, and active user metrics.
- **Events**: Security vulnerability findings, audit log activity, license and vulnerability policy violations, member summaries, and quota usage snapshots.
- **Service Checks**: Health status of quota consumption and API connectivity.

Optional realtime bandwidth metric (disabled by default) can be enabled to emit `cloudsmith.bandwidth_bytes_interval`, representing bytes downloaded over the most recent analytics interval. Enable it by setting `enable_realtime_bandwidth: true` in `cloudsmith.d/conf.yaml`.

With this integration, customers gain centralized observability over their Cloudsmith package infrastructure, helping enforce compliance, troubleshoot issues faster, and optimize resource planning.


## Setup

The Cloudsmith check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Cloudsmith check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-cloudsmith==1.2.0
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `cloudsmith.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Cloudsmith performance data. See the [sample cloudsmith.d/conf.yaml][5] for all available configuration options.

    Example snippet enabling realtime bandwidth:

    ```yaml
     - url: https://api.cloudsmith.io/v1
       cloudsmith_api_key: <API-KEY>
       organization: <ORG-NAME>
       enable_realtime_bandwidth: true
    ```

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `cloudsmith` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

### Events

All Cloudsmith-related events collected appear within the Datadog Event Explorer with the `source:cloudsmith` tag. Events are collected every five minutes to reduce the number of requests sent to the Cloudsmith API.

There are several types of events available:

- Audit Logs event
- Security Scan event
- Vulnerability Policy Violation event
- License Policy Violation event
- Organization Members summary
- Quota (Raw Usage) Summary


## Support

Need help? Contact [Cloudsmith support][10].

[1]: https://cloudsmith.com
[2]: /account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/cloudsmith/datadog_checks/cloudsmith/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/cloudsmith/metadata.csv
[9]: https://github.com/DataDog/integrations-extras/blob/master/cloudsmith/assets/service_checks.json
[10]: https://support.cloudsmith.com/hc/en-us
