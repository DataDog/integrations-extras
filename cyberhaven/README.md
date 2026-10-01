## Overview

Cyberhaven is a Data Detection and Response (DDR) platform that tracks data lineage across endpoints, browsers, and cloud apps, distinguishing genuinely risky data movement from routine activity rather than relying on static content-matching alone. It combines policy-based detection with an AI risk-scoring layer (Linea AI) that assigns a blended risk score per incident and can independently flag severity (`ai_severity`), helping SOC and insider-risk teams triage the highest-risk activity first.

Coverage spans endpoint, browser, and cloud sensors, and extends to physical/offline vectors (removable storage, printers) and collaboration surfaces (email, IM, cloud share, source-code repositories). Every admin and user action inside the Cyberhaven console itself (logins, searches, policy/incident/role/API-key changes) is separately captured as an Audit Log, giving a "who changed what" trail independent of the DLP detection stream.

This integration streams Cyberhaven **Audit Logs**, **Incidents**, and **Events** to Datadog, and includes:

- **Data Streaming**: Cyberhaven forwards each log type to Datadog through a dedicated Streaming Destination (Audit Logs, Incidents, Events).
- **Log Processing**: A Datadog Log Pipeline parses, normalizes, and enriches Cyberhaven data for downstream analysis.
- **Dashboards**: Out-of-the-box dashboards for visualizing parsed and enriched Cyberhaven data.
- **Monitors**: Out-of-the-box monitors to help identify and alert on relevant activities and conditions.


## Setup

### Prerequisites

| Prerequisite | Detail |
|---|---|
| Datadog account | Cloud SIEM enabled; permission to create API keys |
| Cyberhaven admin access | Permission to create and configure streaming destinations |
| Datadog API key | Required. Create one following the steps below |

### Configuration

#### Generate a Datadog API key

1. Log in to your Datadog instance.
2. Click your user avatar in the bottom-left corner and select **Organization Settings**.
3. In the left sidebar, under **Access**, click **API Keys**.
4. Click **New Key**, give it a name (for example, `forwarding-to-cyberhaven`), and click **Create Key**.
5. Copy the generated key and store it safely.

#### Locate your Datadog site

1. Log in to your Datadog instance.
2. Click your user avatar in the bottom-left corner and select **My Preferences**.
3. Note your Datadog site in the top-right corner (for example, `datadoghq.com`).

#### Locate your Cyberhaven instance URL

1. While logged in to your organization's Cyberhaven Console, check your browser's address bar.
2. Note the host domain, which typically follows the pattern `<your-tenant-id>.cyberhaven.io`.

#### Forward logs from Cyberhaven to Datadog

The Cyberhaven Datadog integration supports collection, parsing, and visualization for Audit Logs, Incidents, and Events. Based on your organization's needs, you can configure any single source independently, combine any two, or enable all three.

For each log type, you create a **Destination** (where the logs are sent) and a **Configuration** (what gets sent and when) in the Cyberhaven Console under **Settings > Data Export**.

**Configure Audit Logs**

1. Under **Settings > Data Export**, click **Destinations > Add new**.
2. Name the destination (for example, `audit-logs-to-datadog-destination`).
3. Set **Type** to `HTTPS`.
4. Set **URI** to:

   ```text
   https://http-intake.logs.<YOUR_DATADOG_SITE>/api/v2/logs?ddsource=cyberhaven&ddtags=cyberhaven.domain:<YOUR_CYBERHAVEN_INSTANCE_URL>,cyberhaven.logtype:cyberhaven-audit
   ```

   Replace `<YOUR_DATADOG_SITE>` and `<YOUR_CYBERHAVEN_INSTANCE_URL>` with the values from the steps above.
5. Set **Format** to `JSON Array` and **Encoding** to `GZip`.
6. Under **HTTP Headers**, add a header named `DD-API-KEY` with your Datadog API key as the value.
7. Click **Save & Test**.
8. Under **Settings > Data Export**, click **Configurations > Add new**.
9. Name the configuration (for example, `audit-logs-to-datadog-configuration`).
10. Set **Destination** to the destination created above, **Source** to `Audit`, and **Schedule** to `Immediate`.
11. Ensure **Enabled** is checked, then click **Save**.

**Configure Incident Logs**

1. Repeat steps 1-7 above, naming the destination `incident-logs-to-datadog-destination` and using the logtype tag `cyberhaven.logtype:cyberhaven-incidents` in the URI.
2. Under **Settings > Data Export**, click **Configurations > Add new**.
3. Name the configuration (for example, `incident-logs-to-datadog-configuration`).
4. Set **Destination** to the destination created above, **Source** to `Incidents`, and **Schedule** to `Immediate`.
5. Set **Scope** to `Full Access`.
6. Check **Subscribe to new incidents**, **Subscribe to incident updates**, and **Include incident event details**.
7. Ensure **Enabled** is checked, then click **Save**.

**Configure Event Logs**

1. Repeat steps 1-7 above, naming the destination `events-logs-to-datadog-destination` and using the logtype tag `cyberhaven.logtype:cyberhaven-events` in the URI.
2. Under **Settings > Data Export**, click **Configurations > Add new**.
3. Name the configuration (for example, `events-logs-to-datadog-configuration`).
4. Set **Destination** to the destination created above, **Source** to `Events`, **Schedule** to `Immediate`, and **Scope** to `Full Access`.
5. Ensure **Enabled** is checked, then click **Save**.

### Validation

After saving each configuration, confirm logs are arriving by searching `source:cyberhaven` in the [Log Explorer][1].

## Data Collected

### Logs

The Cyberhaven integration collects Audit Logs, Incidents, and Events, tagged with `source:cyberhaven` and `cyberhaven.logtype:cyberhaven-audit` / `cyberhaven.logtype:cyberhaven-incidents` / `cyberhaven.logtype:cyberhaven-events`.

### Metrics

Cyberhaven does not include any metrics.

### Events

Cyberhaven does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][2] or [Cyberhaven support](mailto:support@cyberhaven.com).

[1]: https://docs.datadoghq.com/logs/explorer/
[2]: https://docs.datadoghq.com/help/
