## Overview

Generator Labs (formerly RBLTracker) provides real-time blacklist monitoring and certificate monitoring.

Connect your [Generator Labs][1] account to Datadog to:

- Push blacklist listing and delisting events from Generator Labs to your dashboard.
- Push certificate monitoring events from Generator Labs to your dashboard.
- Graph and alert on blacklist and certificate metrics.

## Setup

Setting up Generator Labs using a Datadog contact:

1. In Datadog, [copy your API key][2] from the **Organization Settings -> API Keys** section.
2. In [Generator Labs][1], add a new contact from the **Contacts -> Manage -> Contacts** section of the Generator Labs portal and select **Datadog** as the contact type.
3. Paste the Datadog **API Key** and select the **API Endpoint** that matches your Datadog site (US1, US3, US5, EU, AP1, or US1-FED).
4. Select one or more **Contact Groups** for the new contact.

Generator Labs verifies the API key with Datadog when you save the contact, then sends blacklist and certificate alerts to your Datadog events dashboard. See [Datadog Contacts][3] for a full integration guide.

## Data Collected

### Metrics

Generator Labs submits `generatorlabs.rbl.listed_count`, `generatorlabs.rbl.total_checked`, `generatorlabs.cert.expiry_days`, and `generatorlabs.cert.error_count` with its blacklist and certificate alerts. See [Datadog Contacts][3] for the tags on each metric.

### Events

Push your Generator Labs blacklist and certificate events into your [Datadog Event Stream][4]. Filter by `source:generatorlabs` to see only Generator Labs events.

### Service Checks

The Generator Labs integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://generatorlabs.com
[2]: /organization-settings/api-keys
[3]: https://docs.generatorlabs.com/contacts/datadog/
[4]: https://docs.datadoghq.com/events/
[5]: https://docs.datadoghq.com/help/
