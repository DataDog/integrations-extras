# Agent Check: IsDown

## Overview

[IsDown][1] is a status page aggregator & outage monitoring tool that helps businesses stay on top of their critical dependencies. Provide your team real-time monitoring and instant notifications for outages in all your tools and cloud providers. We monitor more than 2000 status pages.

What IsDown offers:

* Get outage alerts in Datadog from all your third-party dependencies ( SaaS, PaaS, Cloud Providers, etc.)
* Understand the frequency of outages through your different providers
* Have the external outages together with the internal information
* Set monitoring for specific parts or the whole provider

## Setup

### IsDown

To connect Datadog to IsDown, you need to generate an API key in Datadog and add it to your IsDown account.

1. Use your existing account or create a new one in [IsDown][1].
2. Log in to your account and go to the Notifications page.
3. Add your API Key and select if you're using the US or EU Datadog site.
4. Click Save.
5. Select the services you want to monitor.
6. In each service you can choose the notification settings.


### Uninstallation

1. Go to the Notifications page in IsDown.
2. Unselect Datadog and click Save.
3. Delete you API Key dedicated to IsDown from Datadog.


## Data Collected

### Service Checks

IsDown sends service checks for each service you monitor. The service check name is `isdown`, with the host being the service name. The status is `OK` if the service is up and `WARNING` or `CRITICAL` depending on the severity of the status of a service.

### Events

IsDown sends events for each outage that happens in the services you monitor. It sends two types of events, one for the start of the outage and one for the end of the outage. The event is send with these attributes:
- Title: The name of the service with the outage title.
- Device Name: The name of the service.
- Text: The description of the outage.
- Tags: `isdown` and `isdown:service_name`.

## Troubleshooting

Need help? Contact [IsDown support][2].

[1]: https://isdown.app
[2]: mailto:support@isdown.app

