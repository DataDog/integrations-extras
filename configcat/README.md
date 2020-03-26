# ConfigCat


## Overview

Ensures that every setting change in ConfigCat is sent to DataDog as an Event.

![DataDogEvent][3]

## Installation
1. Have a <a href="https://www.datadoghq.com/" target="_blank">DataDog subscription.</a>
2. Get a <a href="https://docs.datadoghq.com/account_management/api-app-keys/#api-keys" target="_blank">DataDog API Key.</a>![ApiKey][1]
3. Open the <a href="https://app.configcat.com/product/integrations" target="_blank">integrations tab</a> on ConfigCat Dashboard.
4. Click on DataDog's CONNECT button and set your DataDog API key.
5. You're all set. Go ahead and make some changes on your feature flags then check your Events in DataDog.


## Un-installation
1. Open the <a href="https://app.configcat.com/product/integrations" target="_blank">integrations tab</a> on ConfigCat Dashboard.
2. Click on DataDog's DISCONNECT button and set your DataDog API key.

## DataDog filtering

All configcat related events *source* property is ```configcat``` and tagged with product, config environment names to easy to setup any monitor/alert.

### Example

Search all events where the environment is production: ```sources:configcat production```

![DataDogEvent][4]

## Data Collected

### Metrics

ConfigCat integration does not include any metrics.

### Events

ConfigCat integration sends events from ConfigCat to Datadog.

### Service Checks

ConfigCat integration does not include any service checks.

## Troubleshooting

Need help? Contact [ConfigCat][6].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/assets/images/datadog_apikey.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/assets/images/datadog_connect.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/assets/images/datadog_event.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/assets/images/datadog_filtering.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/configcat/assets/images/datadog_manageproduct.png
[6]: https://configcat.com/docs/integrations/datadog/
[7]: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys


