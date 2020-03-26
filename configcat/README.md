# ConfigCat

![DataDogEvent][3]

## Overview

DataDog integration ensures that all ConfigCat settings changes send to DataDog as an Event. With this feature you can see your system behaviour when changing your settings. You can setup the DataDog integration for a products in the ConfigCat.

## Setup

First of all you need DataDog subscription and [DataDog API key][7].
![DataDogEvent][1]

### 1. Navigate to product's settings page

![DataDogEvent][5]

### 2. Select *Integrations* tab

![DataDogEvent][2]

### 3. Click to DataDog's CONNECT button and set a DataDog API key

## Remove
### 1. Navigate to product's settings page
### 2. Select *Integrations* tab
### 3. Click to DataDog's DISCONNECT button

## DataDog filtering

All configcat related events *source* property is ```configcat``` and tagged with product, config environment names to easy to setup any monitor/alert.

### Example

Search all events where the environment is production: ```sources:configcat production```

![DataDogEvent][4]

## Data Collected

### Metrics

ConfigCat integration does not include any metrics.

### Events


All ConfigCat related events collected appear within the Datadog Event Stream with the `source:configcat` property are  tagged with your product and config environment names. To search all ConfigCat events where the environment is production for instance, use: `sources:configcat production`

![DataDogEvent][4]

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

