# Agent Check: Cloudsmith

## Overview

This check monitors [Cloudsmith][1] through the Datadog Agent.
- Monitor storage, bandwidth, token usage, active members, license policy violations, and security vulnerabilities in your Cloudsmith organization. 


## Setup

The Cloudsmith check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Cloudsmith check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-cloudsmith==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `cloudsmith.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Cloudsmith performance data. See the [sample cloudsmith.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `cloudsmith` under the Checks section.

## Data Collected

### Metrics

This integration provides the following metrics:

- `cloudsmith.storage.percentage_used`: Percentage of storage used.
- `cloudsmith.storage.used_bytes`: Total storage used in bytes.
- `cloudsmith.storage.peak_bytes`: Peak storage usage in bytes.
- `cloudsmith.bandwidth.percentage_used`: Percentage of bandwidth used.
- `cloudsmith.bandwidth.used_bytes`: Total bandwidth used in bytes.
- `cloudsmith.members.total`: Total number of members in the organization.
- `cloudsmith.members.owners`: Total number of owners.
- `cloudsmith.members.managers`: Total number of managers.
- `cloudsmith.members.readers`: Total number of readers.
- `cloudsmith.tokens.total`: Number of entitlement tokens configured.
- `cloudsmith.tokens.active`: Number of active entitlement tokens.
- `cloudsmith.vulnerabilities.total`: Number of vulnerabilities found.
- `cloudsmith.license_policy_violations.total`: Number of license policy violations detected.
- `cloudsmith.vulnerability_policy_violations.total`: Number of vulnerability policy violations detected.

See [metadata.csv][8] for the full list and detailed descriptions.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

### Events

All Cloudsmith-related events collected appear within the Datadog Event Stream with the `source:cloudsmith` property. Events are collected every five minutes to reduce the number of requests sent to the Cloudsmith API.

There are several types of events available:

- Audit Logs event
- Security Scan event
- Vulnerability Policy Violation event
- License Policy Violation event
- Organization Members summary
- Quota (Raw Usage) Summary

They are accessible using the following aggregation keys:

- `@aggregation_key:audit_log`
- `@aggregation_key:vulnerabilities`
- `@aggregation_key:vulnerability_policy_violation`
- `@aggregation_key:license_policy_violation`
- `@aggregation_key:org_members_summary`
- `@aggregation_key:quota_summary`

## Troubleshooting

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
