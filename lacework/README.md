# Agent Check: Lacework

## Overview

Use the Datadog-Lacework integration to forward your Lacework logs and events to Datadog.

## Setup

All configuration happens on Lacework Dashboard. Find details on how to set it up in the [Lacework Documentation][2]. Datadog automatically enables the right logs processing pipeline when it detects Lacework logs.

### Installation

1. In Lacework, go to _Settings_ and select _Integrations_.
2. In the _Outgoing_ section (on the left panel) select Datadog.
3. Fill in the following details:

   - **Name**: Enter a name for the integration. For example, `Datadog-Lacework`.
   - **Datadog Type**: Select the type of logs sent to Datadog:

    | Datadog Type     | Description                                                |
    | ---------------- | ---------------------------------------------------------- |
    | `Logs Details`   | Sends Lacework detailed logs to the Datadog logs platform. |
    | `Logs Summary`   | Sends a Lacework summary to the Datadog logs platform.     |
    | `Events Summary` | Sends a Lacework summary to the Datadog Events platform.   |

   - **Datadog Site**:
     - Select `com` if you use the Datadog US region.
     - Select `eu` if you use the Datadog EU region.
   - **API KEY**: Enter your [Datadog API key][3].
   - **Alert Security Level**: Select the minimum log severity level of forwarded logs

## Data Collected

### Metrics

This Lacework integration does not not collect metrics

### Service Checks

This Lacework intgeration does not include any service checks.

### Log collection

Lacework can be configured to send Logs.

### Events

Lacework can be configured to send Events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://docs.datadoghq.com/integrations/lacework/
[2]: https://www.lacework.com/datadog/
[3]: https://app.datadoghq.com/organization-settings/api-keys
[7]: https://docs.datadoghq.com/help/
