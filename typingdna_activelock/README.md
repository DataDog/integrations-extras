
# TypingDNA ActiveLock

## Overview

[TypingDNA ActiveLock][3] is a Continuous Endpoint Authentication app that helps prevent unauthorized access to your company computers. Once installed on a user's PC, it continuously verifies the user by the way they type. If an unauthorized typing pattern is detected, ActiveLock can instantly lock the computer and log the data to your desired logging platform (such as Datadog).

To visualize your data in Datadog, a custom ActiveLock app needs to be configured and installed. This is the same install for all of your company computers.


## Setup

### Configuration

To get started, navigate to the **Configure** tab on the TypingDNA ActiveLock [integration tile][8].

**I. Generate a Datadog API key**
1. Within your Datadog account, navigate to [Organization settings > API keys][4].
2. Generate a new "API key".

**II. Get your custom install app.**
1. Navigate to [this custom install form][7] and submit your newly generated API key and your Datadog Region (e.g. US1, EU) along with your company details.
2. Once we receive your information, we'll send you a custom ActiveLock app that you'll have to install on your company computers. We'll send any further details over email.
3. After installation, logs should start appearing in [Log explorer][5].

**III. Set up log features (facets/measures).**
1. Once logs flow into Datadog, Navigate to [Log explorer][5].
2. On the left side panel, select the "+Add" button to add the following facets/measures.
Note: Facets and measures are case sensitive. Please include `@` in the path definition.

|Path| Facet or Measure |Type|Display name|
|--|--|--|--|
|`@username`|facet|string|username|
|`@installID`|facet|string|installID|
|`@main_app`|facet|string|main_app|
|`@result`|facet|string|result|
|`@keyboard_id`|facet|string|keyboard_id|
|`@version`|facet|string|version|
| `@score` | measure |integer|score|
| `@speed` | measure |integer|speed|
| `@training_strength` | measure |integer|training_strength|


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

Need help? Contact [Datadog support][1].
Contact [TypingDNA support][2]

[1]: https://docs.datadoghq.com/help/
[2]: https://www.typingdna.com/contact
[3]: https://www.typingdna.com/activelock
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://app.datadoghq.com/logs
[6]: https://app.datadoghq.com/dashboard/lists
[7]: https://forms.gle/3U9KxF7ySThVLDJg8
[8]: https://app.datadoghq.com/integrations/typingdna_activelock
