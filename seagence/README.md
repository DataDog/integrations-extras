# Seagence

## Overview

[Seagence][1] is a defect monitoring platform for Java applications. Using ExecutionPath technology (aka GPS Tracker for transactions), Seagence detects unknown defects caused by various issues like swallowed exceptions, multithreading issues, and others including defects that disguise in a 200 success HTTP response code.

Seagence integrates with Datadog using an API-based integration. Seagence's tiny Java agent is attached to your production application and posts collected data (ExecutionPaths, errors/exceptions, and contextual information) to the Seagence backend. Continuously analyzing the data stream from Seagence's Java agent, Seagence's backend, using ExecutionPath technology, detects defects when they occur, including their root cause, in real-time. This eliminates the need for debugging and troubleshooting. Using a Rest API, Seagence then posts detected defects and their root cause as Datadog Events to the Datadog backend. You can find the details of the defects in the "Seagence - Defects Overview" dashboard or you can set up a Datadog Monitor to trigger alerts. More details about defects can be found on [SeagenceWeb][2]. With a Seagence provided defect and the root cause in hand, you can fix your broken code.

### Usage

The Seagence integration comes with a dashboard called "Seagence - Defects Overview". The top widget shows the defects timeline and the bottom widget shows a list of defects including their root cause exception with complete stack trace. In the defects timeline view, defects are shown as vertical red bars. You can click any vertical bar to open the context menu. Click "View related events" to open the defects as Datadog Events in the "Events Explorer" dashboard.

## Setup

### Installation

Visit [Seagence][1] to sign up for free. Once registered, you can initiate Seagence<->Datadog connection in 2 ways. 1) Find the Seagence tile in Datadog's Integrations view and click "Install Integration". Then click connect button on the tile which will guide you through the Datadog OAUTH2 flow to grant Seagence access to post Events to your Datadog account. 2) Alternatively, login into your Seagence account, goto Settings -> Integrations page and add a Datadog connection. This also guides you through the Datadog OAUTH2 flow to grant Seagence necessary access.

### Configuration
Using -javaagent option, attach Seagence's java agent to your application. Java agent can be downloaded from your Seagence account. For more information, please visit [getting started][3] on [Seagence][1].

### Uninstallation
To remove the Datadog integration from Seagence, navigate to the Seagence's Integrations page and click Revoke. Additionally, uninstall this integration from Datadog by clicking the "Uninstall Integration" button at the bottom on the tile. Once you uninstall this integration, any previous authorizations are revoked. Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys management page.

Also, remove -javaagent option from your application's java runtime parameters. For more information, please visit [getting started][3] on [Seagence][1].

## Data Collected

### Metrics

Seagence does not include any metrics.

### Service Checks

Seagence does not include any service checks.

### Events

Seagence posts an event to datadog upon detecting a defect.

## Support

Need help? Contact [Seagence support][4].


[1]: https://www.seagence.com
[2]: https://app.seagence.com/SeagenceWeb/
[3]: https://seagence.com/product/getting-started/
[4]: mailto:info@seagence.com
