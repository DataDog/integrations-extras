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

Flagsmith does not include any service checks.

### Events

All events are sent to the Datadog event stream.

## Troubleshooting

Need help? Check out the [Flagsmith documentation](https://docs.flagsmith.com/integrations/datadog/) or [contact Datadog Support][4].

[1]: https://www.flagsmith.com/
[2]: https://app.datadoghq.com/account/settings#integrations/flagsmith
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://docs.datadoghq.com/help/
