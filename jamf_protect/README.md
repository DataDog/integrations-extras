# Jamf Protect

## Overview
[Jamf Protect][1] is a comprehensive security solution designed specifically for Apple endpoints, including macOS, iOS and iPadOS endpoints and other supported platforms. Jamf Protect enhances Apple's built-in security features and provides real-time detection of malicious applications, scripts, and user activities. 

Jamf Protect not only detects known malware, adware, but also prevents unknown threats and blocks command and control traffic and risky domains. Furthermore, it provides granular insights into endpoint activity, ensuring endpoint health and compliance, and supports incident response with automated workflows. This integration will collect logs from Jamf Protect events which can be analyzed using Datadog. This integration monitors Jamf Protect logs for both macOS Security and Jamf Security Cloud.

The Jamf Security Cloud data streams, which carry events from Jamf Trust and Jamf's mobile threat defense, content filtering and Zero Trust Network Access (ZTNA) products, send threat events, network traffic, access events, device data, app insights and vulnerability data to Datadog in real time.

## Setup

### Prerequisites

- Datadog intake URL. Use the [Datadog API Logs documentation][7] and select your Datadog Site at the top of the page.
- A [Datadog API key][10].

### Installation

Navigate to the [Integrations page][6] and search for the "Jamf Protect" tile. 

### macOS Security Portal
1. In Jamf Protect, click **Actions**.
2.  Click **Create Actions**.
3.  In the *Action Config Name* field, enter a name (such as `Datadog`).
4.  (Optional) To collect alerts, click **Remote Alert Collection Endpoints** and add the following:

    a. **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=alerts`

    b. Set **Min Severity & Max Severity**.

    c. Click **+ Add HTTP Header** and add the following header:
      ```
      Name: DD-API-KEY
      Value: <API_KEY>
      ```

5. (Optional) To collect unified logs, click **+ Unified Logs Collection Endpoints** and add the following.

    a. **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=unifiedlogs`

    b. Click **+ Add HTTP Header** and add the following header.
      ```
      Name: DD-API-KEY
      Value: <API_KEY>
      ```

6. (Optional) To collect telemetry data, click **+ Telemetry Collection Endpoints**.

    a.  **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=telemetry`

    b.  Click **+ Add HTTP Header** and add the following header.
      ```
      Name: DD-API-KEY
      Value: <API_KEY>
      ```

7. Click **Save**.

### Update your plan to use configured Actions

1. Click **Plans**.
1. Find the plan assigned to devices.
1. Click **Edit** next to the name of the plan.
1. Select the Action from the *Action Configuration* dropdown menu. This is the Action config name that contains the Datadog configuration.
1. Click **Save**.

### (Optional) Jamf Security Cloud

Create one data stream configuration for each type of data you want in Datadog. Each configuration sends one type to one destination. Network traffic, device data and app insights streams can be created only by a Super Admin. A stream sends only events created after it is enabled; earlier events are not exported. Jamf doesn't document what happens to a stream when the admin who created it is removed, so create the streams from an admin account your team owns rather than a personal one.

| Datadog site | Server hostname |
| --- | --- |
| US1 | http-intake.logs.datadoghq.com |
| US3 | http-intake.logs.us3.datadoghq.com |
| US5 | http-intake.logs.us5.datadoghq.com |
| EU1 | http-intake.logs.datadoghq.eu |
| AP1 | http-intake.logs.ap1.datadoghq.com |
| AP2 | http-intake.logs.ap2.datadoghq.com |
| UK1 | http-intake.logs.uk1.datadoghq.com |
| US1-FED | http-intake.logs.ddog-gov.com |
| US2-FED | http-intake.logs.us2.ddog-gov.com |

Repeat these steps for each row of the next table:
1. In Jamf Security Cloud, go to **Integrations** > **Data streams**.
2. Click **Add new**.
3. Select the data stream type, select **Generic HTTP** as the target, and click **Next**.
4. On the Configure data stream page, enter:
   - **Name:** a name you choose, if the console asks for one, for example `Datadog (Network traffic)`
   - **Protocol:** https
   - **Hostname:** your server hostname from the table above
   - **Port:** 443
   - **Endpoint:** `api/v2/logs?ddsource=jamfprotect&service=<SERVICE>`, with the service value from the next table
   - **Additional header:** name `DD-API-KEY`, value your Datadog API key
5. If the console asks for a format, choose JSON. Do not choose CEF (Common Event Format).
6. Click **Test Configuration**, then **Save**, and enable the Configuration mode so the stream starts sending.

| Data stream type | `<SERVICE>` | Notes |
| --- | --- | --- |
| Threat events | `threatevents` | Jamf Protect or Jamf Threat Defense |
| Network traffic | `networktraffic` | Super Admin. Logs every DNS lookup and web request, so volume is high. |
| Access events | `accessevents` | Jamf Connect ZTNA |
| Device data | `devicedata` | Super Admin |
| App insights | `appinsights` | Super Admin |
| Vulnerability data | `vulnerabilitydata` | Apple devices only. Requires Jamf Trust or a configured unified endpoint management (UEM) integration |

Add only the `DD-API-KEY` header; Datadog's logs intake doesn't need an application key.

### Validation

Navigate to the [Logs Explorer][5] and search for `source:jamfprotect` to validate you are receiving logs. For Jamf Security Cloud, search `source:jamfprotect service:<SERVICE>` for each stream you created. Logs appear as Jamf generates events, so a quiet stream can take a while to show its first log. If the `service` attribute isn't populated for threat events or network traffic, filter by `@event.metadata.product` instead (the values are `Threat Events Stream` and `Network Traffic Stream`). The log pipeline was built for threat events and, in part, network traffic; the other four stream types have no dedicated mapping.

## Data Collected

### Logs

The Jamf Protect integration allows you to send [Jamf Audit Logs][4] to Datadog.

| Source | `service` | Data |
| --- | --- | --- |
| macOS Actions | `alerts` | Alerts |
| macOS Actions | `unifiedlogs` | Unified logs |
| macOS Actions | `telemetry` | Telemetry |
| Jamf Security Cloud | `threatevents` | Threat events |
| Jamf Security Cloud | `networktraffic` | Network traffic |
| Jamf Security Cloud | `accessevents` | Access events |
| Jamf Security Cloud | `devicedata` | Device data |
| Jamf Security Cloud | `appinsights` | App insights |
| Jamf Security Cloud | `vulnerabilitydata` | Vulnerability data |

### Metrics

Jamf Protect does not include any metrics.

### Service Checks

Jamf Protect does not include any service checks.

### Events

Jamf Protect does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

A 401 or 403 in Jamf's Test Configuration usually means the API key is missing or wrong. Network traffic can be high volume (it logs every DNS lookup and web request). Datadog bills every log it ingests, even one that an exclusion filter keeps out of the index, so enable this stream only if you need it, and use log exclusion filters to control what is indexed. Scope your own Cloud SIEM rules on `source:jamfprotect` by `service`. To be told when a busy stream such as network traffic stops, create a log monitor on `source:jamfprotect service:<SERVICE>` that alerts when there are no logs for one hour; quieter streams, such as threat events, can go longer without logs, so use a longer window for them.

## Further Reading

Additional helpful documentation, links, and articles:

[Jamf Documentation Integrating Datadog with Jamf Protect][9]

[1]: https://www.jamf.com/products/jamf-protect/
[2]: /account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/
[4]: https://learn.jamf.com/bundle/jamf-protect-documentation/page/Audit_Logs.html
[5]: /logs
[6]: /integrations
[7]: https://docs.datadoghq.com/api/latest/logs/#send-logs
[8]: https://docs.datadoghq.com/getting_started/site/
[9]: https://learn.jamf.com/en-US/bundle/jamf-protect-documentation/page/SecurityIntegration_Datadog.html
[10]: https://docs.datadoghq.com/account_management/api-app-keys/
