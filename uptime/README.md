# Uptime.com

## Overview

Uptime.com is a comprehensive website monitoring service that provides real-time alerts and detailed performance analytics for your web applications and APIs.

The Uptime.com integration with Datadog enhances your monitoring capabilities by combining Uptime.com's monitoring with Datadog's platform. Key functionality includes:

- Uptime.com alerts automatically generate corresponding events in Datadog.
- Datadog events can be assigned lower priority and commented on for tracking.
- Check response times are tracked as metrics in Datadog.
- Metrics update every 5 minutes with 5 data points from 1-minute interval checks.

This integration enables you to proactively identify and resolve performance issues, minimizing downtime and improving overall site reliability.

![Uptime.com Graph][1]

## Setup

### Configuration

To activate the Datadog integration within your Uptime account, go to [Notifications > Integrations][2] then choose Datadog as the provider type when adding a new push notifications profile.

The following describes the fields shown when configuring Datadog within your Uptime account:
shell
- Name: The reference name you desire to assign to your Datadog profile. It can assist you with organizing multiple provider profiles within your Uptime account.

- API key: <span class="hidden-api-key">\${api_key}</span>

- Application Key: <span class="app_key" data-name="uptime"></span>

After configuring your Datadog profile, assign the profile to a contact group located under _Alerting > Contacts_. The profile is assigned in the **Push Notifications** field within the contact group.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this integration.

### Events

The Uptime integration sends an event to your Datadog Event Stream when an alert happens or resolves.

### Service Checks

The Uptime check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/uptime/images/snapshot.png
[2]: https://uptime.com/integrations/manage/
[3]: https://github.com/DataDog/integrations-extras/blob/master/uptime/metadata.csv
[4]: https://docs.datadoghq.com/help/
