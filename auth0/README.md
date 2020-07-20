# Agent Check: auth0

## Overview

Auth0, the identity platform for development teams, provides developers and enterprises with the building blocks they need to secure their applications.


### Integration overview

The integration with Datadog is enabled by Auth0’s Log Streaming. This capability works by sending batches of log events as they are generated in Auth0, giving customers up-to-date information about their Auth0 tenant. Log streaming is capable of delivering 10X more logs, and guarantees delivery with error handling. You can now also release a generic webhook allowing you to deliver near real-time logs to most third-party tools.


#### The integration with Datadog provides a number of important benefits:

Visualize Auth0 Data Without Extra Development Time

One of the key benefits of using Datadog is the ability to collect and visualize data in order to identify trends. Engineering teams use it to visualize error rates and traffic data. Security teams use it to visualize authorization traffic and set up alerts for high-risk actions.


#### Identity data

Identity data provides crucial insight to all of these use cases, allowing teams to better identify problems and make informed decisions.

Make Informed Decisions About System Architecture and Development

By tracking identity trends over time, teams can make informed decisions about product development or system architecture. For example, using authentication data to determine which devices to prioritize development. Likewise, by tracking peak login times and geographies that users are accessing the app from, system architecture teams can determine when and where to scale up resources.


####  Quickly respond to performance and security incidents

In addition to monitoring historical data to spot trends, it is just as important to use identity information to quickly identify security and performance incidents. For instance, massive spikes in unsuccessful login attempts could indicate an ongoing credential stuffing attack, one of the most common threats targeting identity systems.

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
    | `Region` 		   | If you are in the Datadog EU site (app.datadoghq.eu), the Region should be `EU`, otherwise it should be `GLOBAL`   |

	
6. Click Save.

When Auth0 writes the next tenant log, you'll receive a copy of that log event in Datadog with the source and service set to `auth0`.

### Validation

View logs in Datadog:

1. Navigate to **Logs** > **Livetail**.
2. See Auth0 logs by setting `source:auth0`.

## Data Collected

### Logs
Auth0 logs are collected and sent to Datadog. The types of logs that could be returned are outlined [here][5].

### Metrics

auth0 does not include any metrics.

### Service Checks

auth0 does not include any service checks.

### Events

auth0 does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
[2]: https://manage.auth0.com
[4]: https://app.datadoghq.com/account/settings#api
[5]: https://auth0.com/docs/logs/references/log-event-type-codes
