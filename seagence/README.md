# Seagence

## Overview

[Seagence][1] is a defect monitoring platform for Java applications. Using ExecutionPath technology (aka GPS Tracker for transactions), Seagence detects unknown defects caused by various issues like swallowed exceptions, multithreading issues, and others, including defects that are disguised in a 200 success HTTP response code.

With this integration, Seagence continuously analyzes the data stream from the Seagence agent to detect defects when they occur, including the root cause of the defect. When a defect is detected, the integration will send an event to Datadog to alert your team. Using the out-of-the-box dashboard, you have visibility into the detected defects and root causes to eliminate debugging and troubleshooting. More details can be found on [SeagenceWeb][2].

## Setup

### Installation

Visit [Seagence][1] to sign up for free. Once registered, navigate to the Seagence tile on the [Datadog Integrations page][5] and click **Install Integration**. Click **Connect Accounts** on the tile, which guides you through the Datadog OAuth2 flow to grant Seagence access to post Events to your Datadog account.

### Configuration

Using the `-javaagent` option, attach Seagence's Java agent to your application. Download the Java agent from your Seagence account. For more information, visit [getting started][3] on [Seagence][1].

## Uninstallation

To remove the Datadog integration from Seagence:
1. Uninstall the integration from Datadog by clicking **Uninstall Integration**. Once you uninstall the integration, any previous authorizations are revoked.
2. Ensure that all API keys associated with the integration have been disabled by searching for the integration name on the [API Keys Management page][6].
3. Remove the `-javaagent` option from your application's Java runtime parameters.


## Data Collected

### Metrics

Seagence does not include any metrics.

### Service Checks

Seagence does not include any service checks.

### Events

Seagence posts an event to Datadog upon detecting a defect.

## Support

Need help? Contact [Seagence support][4].


[1]: https://www.seagence.com
[2]: https://app.seagence.com/SeagenceWeb/
[3]: https://seagence.com/product/getting-started/
[4]: mailto:info@seagence.com
[5]: https://app.datadoghq.com/integrations/seagence
[6]: https://app.datadoghq.com/organization-settings/api-keys?filter=Seagence
