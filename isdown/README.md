# Agent Check: IsDown

## Overview

[IsDown][1] is a status page aggregator and outage monitoring tool that helps businesses monitor their dependencies. You can provide your team real-time monitoring and instant notifications for outages in all your tools and cloud providers. IsDown monitors more than 2000 status pages.

With this integration, you can receive alerts from third-party dependencies in Datadog, monitor business critical services, and understand the frequency of outages all within the out-of-the-box dashboard.

## Setup

1. Use your existing account or create a new one in [IsDown][1].
2. Log in to your account and go to the **Notifications** page.
3. Click on the checkbox to select Datadog and then click **Connect to Datadog**.
4. You are then redirected to Datadog to authorize the application. IsDown creates an API key that only has access to what IsDown needs to send events and service checks to Datadog.
5. After autorization you will be redirected to IsDown.
6. Select the services you want to monitor.
7. In each service you can choose the notification settings.


### Uninstallation

1. Go to the **Notifications** page in IsDown.
2. Unselect Datadog and click **Save**.
3. Ensure that all API keys associated with this integration have been disabled by searching for IsDown on the [API Keys management page][4] in Datadog.


## Data Collected

### Service Checks

See [service_checks.json][3] for a list of service checks provided by this integration.

### Events

IsDown sends events for each outage that happens in the services you monitor. It sends two types of events, one for the start of the outage and one for the end of the outage. The events are sent with the following attributes:
- Title: The name of the service with the outage.
- Text: The description of the outage.
- Tags: `isdown` and `isdown:service_name`.

## Troubleshooting

Need help? Contact [IsDown support][2].

[1]: https://isdown.app
[2]: mailto:support@isdown.app
[3]: assets/service_checks.json
[4]: https://app.datadoghq.com/organization-settings/api-keys
