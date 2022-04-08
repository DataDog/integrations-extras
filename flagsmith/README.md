# Agent Check: Flagsmith

## Overview

[Flagsmith][1] facilitates feature management across web, mobile, and server side applications. The Datadog Flagsmith integration enables you to view information about flag changes directly within Datadog.

All flag change events are sent to Datadog. These events are tagged with the environment they were changed in.

## Setup

In the [Flagsmith Integration tile][2], enter your [Datadog API Key][3]. For API URL, enter `https://api.datadoghq.com` if you are using the US site, or `https://api.datadoghq.eu` if you are using the EU site.

## Data Collected

### Metrics

The Flagsmith integration does not include any metrics.

### Service Checks

The Flagsmith integration does not include any service checks.

### Events

All Flagsmith events are sent to the Datadog event stream.

## Troubleshooting

Need help? See the [Flagsmith documentation][4] or contact [Datadog Support][5].

[1]: https://www.flagsmith.com/
[2]: https://app.datadoghq.com/account/settings#integrations/flagsmith
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://docs.flagsmith.com/integrations/datadog/
[5]: https://docs.datadoghq.com/help/
