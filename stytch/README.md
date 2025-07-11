# Agent Check: Stytch

## Overview

[Stytch][1] is an all-in-one platform for modern authentication, providing authentication, authorization, and fraud detection that adapts with your code base, your customers and threat vectors.  

This integration leverages Stytch's [Event log streaming][2] to send logs directly to Datadog in real-time, allowing you to:
* Analyze and get deeper insights into your event logs within Datadog's logging platform
* Control log retention beyond the default retention window in Stytch
* Let your admins troubleshoot failed logins quickly and easily for your end users by filtering on specific IDs in your logs
* Set up alerts on your event logs: For example, a spike in auth failures and SMS sends might indicate a potential toll fraud attack

## Setup

### Installation

All configuration occurs within the [Stytch Dashboard][3].

1. Under the **Activity** tab in the Stytch dashboard, navigate to **Stream Settings**.
2. Select **Datadog** from the list of Destinations in the dropdown.
3. Fill in your Datadog [site][4] and [API key][5].
4. Toggle on **Enable event log streaming** and save the changes.

Logs will be pushed to Datadog in several minutes.

### Validation

View logs in Datadog:

1. Navigate to the Logs [Live Tail][6].
2. View your Stytch event logs by filtering over `source:stytch`.

## Data Collected

### Metrics

Stytch does not include any metrics.

### Service Checks

Stytch does not include any service checks.

### Events

Stytch does not include any events.

### Logs

Stytch event logs are collected and sent to your Datadog organization. For more information on log schema and metadata, please refer to [Stytch's event logs documentation][7].

## Troubleshooting

Need help? Contact [Datadog support][8].

[1]: https://stytch.com
[2]: https://stytch.com/docs/workspace-management/event-log-streaming
[3]: https://stytch.com/dashboard
[4]: https://docs.datadoghq.com/getting_started/site/
[5]: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys
[6]: https://docs.datadoghq.com/logs/explorer/live_tail/
[7]: https://stytch.com/docs/workspace-management/event-logs
[8]: https://docs.datadoghq.com/help/

