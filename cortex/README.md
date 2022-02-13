# Agent Check: cortex

## Overview

The [Cortex][1] integration enables you to trigger Datadog incidents directly from the Cortex dashboard.

## Setup

To set up this integration, you must have a Cortex account, along with Datadog API and Application keys.

### Configuration

1. Contact Cortex for a demo if not a current customer.
2. Create a [Datadog API key][2].
3. Create a [Datadog Application key][3].
4. Add Datadog API and Application keys to the [Cortex Datadog Integration][4].

### Validation

1. Go to the [Cortex homepage][5].
2. Click on an existing service or [create a new service][6].
3. On the sidebar under "INTEGRATIONS", click "See all" and choose "Datadog".
4. Click the red "Trigger Incident" button above "Incidents".
5. Fill in information in the form and click green "Trigger Incident" button.
6. You should get a message on screen that says: "Incident has been triggered! Click here to see it in Datadog."
7. Additionally, the new incident should be displayed under "Incidents".

## Data Collected

### Metrics

Cortex does not include any metrics.

### Service Checks

Cortex does not include any service checks.

### Events

Cortex does not include any events.

## Troubleshooting

Need help? Contact [support@getcortexapp.com](mailto:support@getcortexapp.com).

[1]: https://www.getcortexapp.com/
[2]: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#application-keys
[4]: https://app.getcortexapp.com/admin/settings/datadog
[5]: https://app.getcortexapp.com/admin/index
[6]: https://app.getcortexapp.com/admin/service/new
