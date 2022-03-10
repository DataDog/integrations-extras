# Agent Check: auth0

## Overview

Auth0 is an identity platform for development teams which provides developers and enterprises with the building blocks they need to secure their applications.


This integration leverages Auth0's Log Streaming to send logs directly to Datadog. The logs are sent in real time as they are generated in Auth0, giving customers up-to-date information about their Auth0 tenant. One of the key benefits of using using this integration is the ability to collect and visualize data in order to identify trends. Engineering teams use it to visualize error rates and traffic data. Security teams use it to visualize authorization traffic and set up alerts for high-risk actions.

### Key use cases

#### Correlate activity with identity data to surface trends

Identity data provides crucial insight into who performed what activity. This allows teams to better understand user behavior across their system.

#### Decisions about system architecture and development

By tracking identity trends over time, teams can make informed decisions about product development and system architecture. As an example teams might prioritize development based on tracking peak login times, authentication activity and geographical activity.

####  Quickly respond to performance and security incidents

Identity information can be used to quickly identify security and performance incidents. For instance, massive spikes in unsuccessful login attempts could indicate an ongoing credential stuffing attack, one of the most common threats targeting identity systems.

By configuring thresholds, security teams can set up alerts to notify them when suspicious events take place, allowing them to more quickly respond to security incidents.

## Setup

All configuration happens on the [Auth0 Dashboard][2]. 

1. Log in to the [Auth0 Dashboard][2].
2. Navigate to **Logs** > **Streams**.
3. Click **+ Create Stream**.
4. Select Datadog and enter a unique name for your new Datadog Event Stream.
5. On the next screen, provide the following settings for your Datadog Event Stream:


    | Setting     	   | Description                                                |
    | ---------------- | ---------------------------------------------------------- |
    | `API Key`        | Enter your [Datadog API key][4]. 							|
    | `Region` 		     | Your [Datadog site][7]. For example, `EU` for app.datadoghq.eu, `US1` for app.datadoghq.com, and `US3` for us3.datadoghq.com. |

	
6. Click Save.

When Auth0 writes the next tenant log, you receive a copy of that log event in Datadog with the source and service set to `auth0`.

### Validation

View logs in Datadog:

1. Navigate to **Logs** > **Livetail**.
2. See Auth0 logs by setting `source:auth0`.

## Data Collected

### Log collection

Auth0 logs are collected and sent to Datadog. The types of logs that could be returned are outlined in the [Log Event Type Codes][5].

### Metrics

auth0 does not include any metrics.

### Service Checks

auth0 does not include any service checks.

### Events

auth0 does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].
Read more about this integration in our [blog post][6].

[1]: https://docs.datadoghq.com/help/
[2]: https://manage.auth0.com
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://auth0.com/docs/logs/references/log-event-type-codes
[6]: https://www.datadoghq.com/blog/monitor-auth0-with-datadog/
[7]: https://docs.datadoghq.com/getting_started/site/
