# Uptime.com

## Overview

Get events and metrics from your app in real time to:

* Track and notify of any downtime or interruptions.
* Visualize response time metrics from synthetic requests.

![Uptime.com Graph][1]

## Setup

### Configuration

In order to activate the integration of Datadog within your Uptime account, go to [Alerting>Push Notifications][2] then choose Datadog as the provider type when adding a new push notifications profile.

The following describes the fields shown when configuring Datadog within your Uptime account: 

* Name: The reference name you desire to assign to your Datadog profile. It can assist you with organizing multiple provider profiles within your Uptime account.

* API key: <span class="hidden-api-key">${api_key}</span>

* Application Key: <span class="app_key" data-name="uptime.com"></span> 

<li>Once you've configured your Datadog profile, you will need to assign the profile to a contact group located under Alerting>Contacts. The profile is assigned at the Push Notifications field within the contact group.</li> 
</ul>

## Data Collected
### Metrics
See [metadata.csv][3] for a list of metrics provided by this integration.

### Events
The Uptime check does not include any events at this time.

### Service Checks
The Uptime check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][4].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/ilan/uptime/uptime/images/snapshot.png
[2]: https://uptime.com/push-notifications/manage/
[3]: https://github.com/DataDog/integrations-extras/blob/master/uptime/metadata.csv
[4]: http://docs.datadoghq.com/help/
