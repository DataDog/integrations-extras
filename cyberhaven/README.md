## Overview

This integration streams Cyberhaven **Audit Logs**, **Incidents**, and **Events** to Datadog, where they are parsed, enriched, and ready to search, visualize, and alert on. It includes:

- **Data Streaming**: Cyberhaven forwards each log type to Datadog through its own Destination and Configuration (Audit Logs, Incidents, Events).
- **Log Processing**: A Datadog log pipeline parses, normalizes, and enriches each log type, with a separate sub-pipeline for each. Incident logs also get a `cyberhaven.incident.url` attribute that links straight to the incident in Cyberhaven.
- **Dashboards**: Four out-of-the-box dashboards. **Audit**, **Incidents**, and **Events** let you analyze each log type (the Incidents dashboard links each incident to Cyberhaven). **Troubleshooting** shows whether data is flowing and processed correctly, with step-by-step fixes.
- **Monitors**: Three monitor templates, one per log type, that you enable for the log types you stream. Each alerts when no logs have been received for 24 hours.

### About Cyberhaven

Cyberhaven is a Data Detection and Response (DDR) platform that tracks data lineage across endpoints, browsers, and cloud apps, distinguishing genuinely risky data movement from routine activity rather than relying on static content-matching alone. It combines policy-based detection with an AI risk-scoring layer (Linea AI) that assigns a risk score per incident, helping SOC and insider-risk teams triage the highest-risk activity first.

Coverage spans endpoint, browser, and cloud sensors, and extends to physical and offline vectors (removable storage, printers) and collaboration surfaces (email, IM, cloud share, source-code repositories). Every admin and user action in the Cyberhaven console itself (logins, searches, policy, incident, role, and API-key changes) is captured as an Audit Log, giving a "who changed what" trail independent of the detection stream.

## Setup

### Prerequisites

| Prerequisite | Detail |
|---|---|
| Datadog account | Permission to create API keys |
| Cyberhaven admin access | Permission to create and configure streaming destinations |

### Step 1: Gather three values

Collect these before you open the Cyberhaven Console.

| Value | Used as | Where to find it |
|---|---|---|
| Datadog API key | `DD-API-KEY` header | In Datadog, click your avatar (bottom-left) > **Organization Settings** > **Access** > **API Keys** > **New Key**. Name it (for example, `forwarding-to-cyberhaven`), click **Create Key**, and copy the key. |
| Datadog site | `<YOUR_DATADOG_SITE>` | In Datadog, click your avatar > **My Preferences**. The site is shown in the top-right corner (for example, `datadoghq.com`). |
| Cyberhaven instance URL | `<YOUR_CYBERHAVEN_INSTANCE_URL>` | In the Cyberhaven Console, check your browser's address bar. It typically follows the pattern `<your-tenant-id>.cyberhaven.io`. Enter the host only, without `https://` or a path. |

The Cyberhaven instance URL is also used to build the incident links in Datadog, so a wrong value breaks them.

### Step 2: Quick start with Incidents

Start with Incidents to get data flowing and confirm it end to end. Once it works, adding Audit Logs and Events (Step 3) takes the same steps with a few different values.

Cyberhaven needs a **Destination** (where logs are sent) and a **Configuration** (what is sent and when). Both are under **Settings > Data Export** in the Cyberhaven Console.

**Create the destination**

1. Click **Destinations > Add new**.
2. Name it `incident-logs-to-datadog-destination`.
3. Set **Type** to `HTTPS`.
4. Set **URI** to the following, replacing the two placeholders with your values from Step 1:

   ```text
   https://http-intake.logs.<YOUR_DATADOG_SITE>/api/v2/logs?ddsource=cyberhaven&ddtags=cyberhaven.domain:<YOUR_CYBERHAVEN_INSTANCE_URL>,cyberhaven.logtype:cyberhaven-incidents
   ```
5. Set **Format** to `JSON Array` and **Encoding** to `GZip`.
6. Under **HTTP Headers**, add a header named `DD-API-KEY` with your Datadog API key as the value.
7. Click **Save & Test**.

**Create the configuration**

1. Click **Configurations > Add new**.
2. Name it `incident-logs-to-datadog-configuration`.
3. Set **Destination** to the destination you just created, **Source** to `Incidents`, **Schedule** to `Immediate`, and **Max records per request** to `100`.
4. Set **Scope** to `Full Access`.
5. Check **Subscribe to new incidents**, **Subscribe to incident updates**, and **Include incident event details**.
6. Ensure **Enabled** is checked, then click **Save**.

**Verify**

In the [Log Explorer][1], search `source:cyberhaven cyberhaven.logtype:cyberhaven-incidents`. Logs appear as new incidents are created or updated. If nothing shows up after a few minutes, open the **Cyberhaven - Troubleshooting** dashboard, or see the Support section below.

### Step 3: Add Audit Logs and Events (optional)

You can configure any single log type, combine any two, or enable all three. Repeat the Step 2 procedure for each additional log type, changing only the values below. Everything else (Type, URI pattern, Format, Encoding, `DD-API-KEY` header, Schedule, Max records, Enabled) stays the same.

| | Audit Logs | Incidents (done in Step 2) | Events |
|---|---|---|---|
| Destination name | `audit-logs-to-datadog-destination` | `incident-logs-to-datadog-destination` | `event-logs-to-datadog-destination` |
| `cyberhaven.logtype` value in the URI | `cyberhaven-audit` | `cyberhaven-incidents` | `cyberhaven-events` |
| Configuration name | `audit-logs-to-datadog-configuration` | `incident-logs-to-datadog-configuration` | `event-logs-to-datadog-configuration` |
| Configuration **Source** | `Audit` | `Incidents` | `Events` |
| Configuration **Scope** | Not applicable | `Full Access` | `Full Access` |
| Extra options | None | **Subscribe to new incidents**, **Subscribe to incident updates**, **Include incident event details** | None |

Each log type needs its own destination, because the `cyberhaven.logtype` tag in the URI is what the Datadog pipeline uses to process it correctly.

To verify each one, search `source:cyberhaven cyberhaven.logtype:<value>` in the [Log Explorer][1], using the value from the table.

### Step 4: Enable monitors (optional)

The integration provides three monitor templates, one per log type. They are templates, so none is active until you create it, and you only create the ones for log types you stream. A monitor for a log type you have not set up would alert after 24 hours with no logs.

| Monitor template | Create it if you completed |
|---|---|
| [Cyberhaven] Audit logs not received in Datadog | Audit Logs (Step 3) |
| [Cyberhaven] Incident logs not received in Datadog | Incidents (Step 2) |
| [Cyberhaven] Event logs not received in Datadog | Events (Step 3) |

1. In Datadog, go to **Monitors > Templates** and search for `Cyberhaven`.
2. Open the template for each log type you stream and click **Create Monitor**.
3. Under **Notify your team**, add the people or channels to alert (for example, `@your-team-email` or `@slack-your-channel`), then click **Create**.

Each monitor alerts when no logs of that type have been received for 24 hours. Quiet periods can be normal, especially for Incidents (no policy matched) and Audit Logs (no console activity). If this is noisy for you, lower the monitor's priority or lengthen its evaluation window.

## Data Collected

### Logs

The Cyberhaven integration collects Audit Logs, Incidents, and Events, tagged with `source:cyberhaven` and `cyberhaven.logtype:cyberhaven-audit` / `cyberhaven.logtype:cyberhaven-incidents` / `cyberhaven.logtype:cyberhaven-events`.

Incident logs include `cyberhaven.incident.url`, a link that opens the incident in your Cyberhaven Console. It is shown in the Incidents dashboard (**Incident Links**) and can be used in monitors and notebooks.

### Metrics

Cyberhaven does not include any metrics.

### Events

Cyberhaven does not include any events.

## Support

If logs are missing or not processed correctly, open the **Cyberhaven - Troubleshooting** dashboard. It shows whether each log type is arriving, whether records are tagged and processed correctly, and gives step-by-step fixes for the most common problems.

The most common causes are:

- A wrong Datadog site or an invalid `DD-API-KEY` in the destination (**Save & Test** shows an error).
- A wrong `ddsource` or `cyberhaven.logtype` value in the destination URI.
- **Format** not set to `JSON Array` or **Encoding** not set to `GZip`.
- The configuration is not **Enabled**, or points at the wrong destination.

Need help? Contact [Datadog support][2] or [Cyberhaven support](mailto:support@cyberhaven.com).

[1]: https://docs.datadoghq.com/logs/explorer/
[2]: https://docs.datadoghq.com/help/