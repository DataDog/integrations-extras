# Agent Check: Flagsmith

## Overview

[Flagsmith][https://www.flagsmith.com/] facilitates feature management across web, mobile, and server side applications. The Datadog Flagsmith integration enables you to view information about flag changes directly within Datadog.

All flag change events are sent to Datadog. These events are tagged with the environment they were changed in.

## Setup

1. Sign up to DataDog and Flagsmith. Log into both accounts.
2. Get your [Datadog API Key][1].
3. In the Integrations area of Flagsmith, expand the Datadog integration and enter your API key and API URL (either [https://api.datadoghq.eu/](https://api.datadoghq.eu/) or [https://api.datadoghq.com/](https://api.datadoghq.com/)).
4. You're done. Change a flag in the Flagsmith dashboard and see the event appear within the Datadog control panel.

## Removal

Simply navigate to the Integration page within Flagsmith and click the trash can icon.

## Data Collected

### Metrics

No data is collected other than the flag event information that is sent to Datadog.

### Service Checks

Flagsmith does not include any service checks.

### Events

Flagsmith does not include any events.

## Troubleshooting

Need help? Check out our [documentation](https://docs.flagsmith.com/integrations/datadog/) or [contact us][https://www.flagsmith.com/].

[1]: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys
