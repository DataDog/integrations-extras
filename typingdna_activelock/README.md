
# TypingDNA ActiveLock

## Overview

[TypingDNA ActiveLock][3] is a Continuous Endpoint Authentication app that helps prevent unauthorized access to your company computers by detecting typing patterns and locking computers to protect sensitive data.

This integration allows you to send logs from your ActiveLock apps to Datadog, and provides an out-of-the-box dashboard to monitor your organizations computers.

To visualize your data in Datadog, a custom ActiveLock app needs to be configured and installed. This is the same install for all of your company computers.


## Setup

### Configuration

To generate a Datadog API key:

1. Navigate to [Organization settings > API keys][4] in your Datadog account.
2. Click **+ New Key** to generate an API key.

To get your custom install app:

1. Complete [this custom install form][7] by submitting your newly generated API key, [Datadog site][9], and your company details.
2. You will receive an email including a custom ActiveLock app to install on your company computers, and installation instructions. 
	a. This install has an initial limit of 10 seats, and comes with a default 30-day trial period. To remove trial limitations you need a full commercial license. If you don't have a commercial license already, contact [TypingDNA][2] for licensing or the reseller/partner through which you found us.
3. After installation, your ActiveLock logs should start to appear in [Log Explorer][5].

Note: If you are through a reseller/partner, please follow their instructions to get your custom install app (and commercial license).


### Validation

To view your ActiveLock logs in Datadog, navigate to the [Log Explorer][5] and enter `source:typingdna` and/or `service:activelock` in the search query.

To access the dashboard, navigate to the [Dashboard List][6] and search for the **TypingDNA ActiveLock** dashboard.


## Data Collected

### Log collection

TypingDNA ActiveLock logs are collected and sent to Datadog directly from each application.

## Troubleshooting

Need help? Contact [Datadog][1] or [TypingDNA support][2].

[1]: https://docs.datadoghq.com/help/
[2]: https://www.typingdna.com/contact
[3]: https://www.typingdna.com/activelock
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://app.datadoghq.com/logs
[6]: https://app.datadoghq.com/dashboard/lists
[7]: https://www.typingdna.com/clients/altrial
[8]: https://app.datadoghq.com/integrations/typingdna_activelock
[9]: https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site
