# Agent Check: Flagsmith

## Overview

[Flagsmith][https://www.flagsmith.com/] facilitates feature management across web, mobile, and server side applications. The Datadog Flagsmith integration enables you to view information about flag changes directly within Datadog.

All flag change events are sent to Datadog. These events are tagged with the environment they were changed in.

## Setup

In the [Flagsmith Integration tile][https://app.datadoghq.com/account/settings#integrations/flagsmith], enter your [Datadog API Key][https://app.datadoghq.com/account/settings#api]. For API URL, enter `https://api.datadoghq.com` if you are using the US site, or `https://api.datadoghq.eu` if you are using the EU site.

## Removal

Simply navigate to the Integration page within Flagsmith and click the trash can icon.

## Data Collected

### Metrics

The Flagsmith integration does not include any metrics.

### Service Checks

Flagsmith does not include any service checks.

### Events

All events are sent to the Datadog event stream.

## Troubleshooting

Need help? Check out the [Flagsmith documentation](https://docs.flagsmith.com/integrations/datadog/) or [contact Datadog Support][https://docs.datadoghq.com/help/].

[1]: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys
