
# TypingDNA ActiveLock

## Overview

[TypingDNA ActiveLock][3] is a Continuous Endpoint Authentication app that helps prevent unauthorized access to your company computers. Once installed on a user's PC, it continuously verifies the user by the way they type. If an unauthorized typing pattern is detected, ActiveLock instantly locks the computer and/or logs the data to your desired logging platform (i.e. Datadog).

To visualize your data in Datadog, a custom ActiveLock app will need to be configured and installed. Note: This will be the same install for all of your company computers.

Configuration is straightforward and takes few minutes, please follow the steps in the *Configure* tab to get started.

## Setup

### Configuration

There are 3 main parts of the setup.

**1. Generate a Datadog API key**
Within your Datadog account, go to [Organization settings > API keys][4] and generate a new key.

**2. Get your custom install app.**
Send your newly generated API key AND your Datadog Region (e.g. US1, EU), to your TypingDNA account manager, and/or to datadog.support@typingdna.com. Once we receive your API key and Region, we'll send you a custom install app that you'll have to install on your company computers. New logs will start appearing in [Log explorer][5].

**3. Set up log features (facets/measures).**
Now, once your data starts to log in Datadog, for ActiveLock dashboard to work correctly you'll need to set up a few more things. From [Log explorer][5], you'll need to add the following facets/measures (case sensitive) from the left side panel, *+Add* button. It is important to use `@` in the path definition.

|Path| Facet/Measure |Type|Display name|
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

To view your ActiveLock logs in Datadog, navigate to [Log explorer][5] and set `source:typingdna_activelock`

To open the dashboard, navigate to [All Dashboards][6] where you should find the **TypingDNA ActiveLock** dashboard.


## Data Collected

### Log collection

TypingDNA ActiveLock logs are collected and sent to Datadog directly from each app.

In order to be able to view the logs correctly in the TypingDNA ActiveLock dashboard you will need to set the facets and measures exactly as in the Configuration steps.

### Metrics

TypingDNA ActiveLock does not include any metrics.

### Service Checks

TypingDNA ActiveLock does not include any service checks.

### Events

TypingDNA ActiveLock does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].
Contact [TypingDNA support][2] or send email to datadog.support@typingdna.com.

[1]: https://docs.datadoghq.com/help/
[2]: https://www.typingdna.com/contact
[3]: https://www.typingdna.com/activelock
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://app.datadoghq.com/logs
[6]: https://app.datadoghq.com/dashboard/lists
