# Seagence

## Overview

[Seagence][1] is a production-grade Realtime Defect Detection and Resolution tool for Java applications. Using ExecutionPath technology, Seagence detects known and unknown defects caused by various issues like multithreading issues, swallowed, handled, and unhandled exceptions, and others, including defects that are disguised in a 200 success HTTP response code.

With this integration, Seagence backend continuously analyzes the data stream from the Seagence agent to detect defects when they occur, including the root cause of the defect. When a defect is detected, the integration will send an event to Datadog to alert your team. Using the out-of-the-box dashboard, you have visibility into the detected defects and root causes to eliminate debugging and troubleshooting. More details about the defect can be found on [SeagenceWeb][2].

## Setup

### Installation

Visit [Seagence][1] to sign up for free. Once registered, navigate to the Seagence tile on the [Datadog Integrations page][5] and click **Install Integration**. Click **Connect Accounts** on the tile, which guides you through the Datadog OAuth2 flow to grant Seagence access to post Events to your Datadog account.

After connecting your accounts, go to the "Assets" tab on the tile. Click **Recommended Monitors** > **Seagence Defect Detection Monitor**. This will redirect you to create the out-of-the-box monitor. Click **Create** at the bottom of the page to install the Seagence monitor.

### Configuration

Using the `-javaagent` option, attach Seagence's Java agent to your application. Download the Java agent from your Seagence account. For more information, visit [getting started][3] on [Seagence][1].

## Uninstallation

To remove the Datadog integration from Seagence:
1. Uninstall the integration from Datadog by clicking **Uninstall Integration**. Once you uninstall the integration, any previous authorizations are revoked.
2. Ensure that all API keys associated with the integration have been disabled by searching for the integration name on the [API Keys Management page][6].
3. Delete the associated monitor by going to **Monitors** > **Manage Monitors**. Hover over **Seagence Defect Detection Monitor** and click **Delete**.
4. Remove the `-javaagent` option from your application's Java runtime parameters.


## Data Collected

### Metrics

Seagence does not include any metrics.

### Service Checks

Seagence does not include any service checks.

### Events

Seagence posts an event to Datadog upon detecting a defect.

## Support

Need help? Contact [Seagence support][4].

## Further Reading

Additional helpful documentation, links, and articles:

- [Detect Java code-level issues with Seagence and Datadog][7]

[1]: https://www.seagence.com
[2]: https://app.seagence.com/SeagenceWeb/
[3]: https://seagence.com/product/getting-started/
[4]: mailto:support@seagence.com
[5]: https://app.datadoghq.com/integrations/seagence
[6]: https://app.datadoghq.com/organization-settings/api-keys?filter=Seagence
[7]: https://www.datadoghq.com/blog/seagence-datadog-marketplace/
