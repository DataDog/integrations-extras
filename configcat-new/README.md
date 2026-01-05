# ConfigCat

## Overview

Manage features and change your software configuration using [ConfigCat feature flags][2], without the need to re-deploy code. A [10 minute trainable Dashboard][5] allows even non-technical team members to manage features directly. Deploy anytime, release when confident. Target a specific group of users first with new ideas. Supports A/B/n testing and soft launching. Provides [open-source SDKs][11] for easy integration with any web, mobile or backend application.

This integration ensures that every setting change in ConfigCat is sent to Datadog as an Event.

*Example:*
![DatadogEvent][3]

## Setup

1. Have a [Datadog subscription][8].
2. Get a [Datadog API Key][9].
    ![DatadogEvent][1] 
4. Open the [integrations tab][10] on ConfigCat Dashboard.
5. Click on Datadog's _CONNECT_ button and set your Datadog API key.
6. You're all set. Go ahead and make some changes on your feature flags then check your Events in Datadog.


### Un-installation

1. Open the [integrations tab][10] on ConfigCat Dashboard.
2. Click on Datadog's DISCONNECT button and set your Datadog API key.

## Data Collected

### Metrics

ConfigCat integration does not include any metrics.

### Events

All ConfigCat related events collected appear within the Datadog Event Stream with the `source:configcat` property are tagged with your product, config and environment names.

For example here is how to search for events that happened in the production environment: `source:configcat production`:

![Filtering][4]

### Service Checks

ConfigCat integration does not include any service checks.

## Troubleshooting

Need help? See the [ConfigCat documentation][6] or contact [ConfigCat support][7].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/images/datadog_apikey.png
[2]: https://configcat.com
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/images/datadog_event.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/images/datadog_filtering.png
[5]: https://app.configcat.com
[6]: https://configcat.com/docs/integrations/datadog/
[7]: https://configcat.com/support
[8]: https://www.datadoghq.com
[9]: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys
[10]: https://app.configcat.com/product/integrations
[11]: https://github.com/configcat
