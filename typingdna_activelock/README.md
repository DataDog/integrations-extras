

# TypingDNA ActiveLock

## Overview

[TypingDNA ActiveLock][3] is a Continuous Endpoint Authentication app that helps prevent unauthorized access to your company computers. Once installed on a user's PC, it continuously verifies the user by the way they type. If an unauthorized typing pattern is detected, ActiveLock can instantly lock the computer and log the data to your desired logging platform (such as Datadog).

To visualize your data in Datadog, a custom ActiveLock app needs to be configured and installed. This is the same install for all of your company computers.


## Setup

### Configuration

To generate a Datadog API key:

1. Navigate to [Organization settings > API keys][4] in your Datadog account.
2. Click **+ New Key** to generate an API key.

To get your custom install app:

1. Complete [this custom install form][7] by submitting your newly generated API key and Datadog site region (such as US1 or EU), along with your company details.
2. You will then receive a custom ActiveLock app that you can install on your company computers and more information over email.
3. After installation, your ActiveLock logs should start to appear in [Log Explorer][5].



### Validation

To view your ActiveLock logs in Datadog, navigate to the [Log Explorer][5] and enter `source:typingdna_activelock` in the search query.

To access the dashboard, navigate to the [Dashboard List][6] and search for the **TypingDNA ActiveLock** dashboard.


## Data Collected

### Log collection

TypingDNA ActiveLock logs are collected and sent to Datadog directly from each application.

In order to view the logs correctly in the TypingDNA ActiveLock dashboard, you need to set the facets and measures in the [Configuration](#configuration) section.

### Metrics

The TypingDNA ActiveLock integration does not include any metrics.

### Events

The TypingDNA ActiveLock integration does not include any events.

### Service Checks

The TypingDNA ActiveLock integration does not include any service checks.


## Troubleshooting

Need help? Contact [Datadog][1] or [TypingDNA support][2].

[1]: https://docs.datadoghq.com/help/
[2]: https://www.typingdna.com/contact
[3]: https://www.typingdna.com/activelock
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://app.datadoghq.com/logs
[6]: https://app.datadoghq.com/dashboard/lists
[7]: https://forms.gle/3U9KxF7ySThVLDJg8
[8]: https://app.datadoghq.com/integrations/typingdna_activelock
