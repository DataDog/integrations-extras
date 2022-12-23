# Agent Check: IsDown

## Overview

[IsDown][1] is a status page aggregator and outage monitoring tool that helps businesses monitor their dependencies. You can provide your team real-time monitoring and instant notifications for outages in all your tools and cloud providers. IsDown monitors more than 2000 status pages.

With this integration, you can receive alerts from third-party dependencies in Datadog, monitor business critical services, and understand the frequency of outages all within the out-of-the-box dashboard.

## Setup

### IsDown

To connect Datadog to IsDown, you need to generate an [API key][5] in Datadog and add it to your IsDown account.

1. Use your existing account or create a new one in [IsDown][1].
2. Log in to your account and go to the Notifications page.
3. Add your API Key and select if you're using the US or EU [Datadog site][4].
4. Click Save.
5. Select the services you want to monitor.
6. In each service you can choose the notification settings.


### Uninstallation

1. Go to the **Notifications** page in IsDown.
2. Unselect Datadog and click **Save**.
3. In Datadog, delete your API Key dedicated to IsDown.


## Data Collected

### Service Checks

See [service_checks.json][3] for a list of service checks provided by this integration.

### Events

IsDown sends events for each outage that happens in the services you monitor. It sends two types of events, one for the start of the outage and one for the end of the outage. The events are sent with the following attributes:
- Title: The name of the service with the outage title.
- Device Name: The name of the service.
- Text: The description of the outage.
- Tags: `isdown` and `isdown:service_name`.

## Troubleshooting

Need help? Contact [IsDown support][2].

[1]: https://isdown.app
[2]: mailto:support@isdown.app
[3]: assets/service_checks.json

