# Agent Check: auth0

## Overview

Use the Datadog-Auth0 integration to view and analyze your log events from Auth0.

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

[1]: https://docs.datadoghq.com/help
[2]: https://manage.auth0.com
[4]: https://app.datadoghq.com/account/settings#api
[5]: https://auth0.com/docs/logs/references/log-event-type-codes
