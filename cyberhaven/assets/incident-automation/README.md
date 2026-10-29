# Cyberhaven incidents in Datadog Incident Management

Automatically create and update a **Datadog Incident** for every Cyberhaven incident, using the logs the Cyberhaven integration already streams into Datadog.

This is optional. The Cyberhaven integration works without it. Set it up only if you want Cyberhaven incidents to appear in Datadog Incident Management.

## How it works

```
Cyberhaven incident created or updated
        |  (Incidents data export, Cyberhaven integration)
        v
Incident log in Datadog   source:cyberhaven cyberhaven.logtype:cyberhaven-incidents
        |
        v
Monitor  [Cyberhaven] Incident created or updated
        |  one alert per incident version (@cyberhaven.incident.id + @cyberhaven.incident.last_modified)
        v
Workflow  cyberhaven-create-update-incident
        |  1. reads the incident id from the alert
        |  2. loads that incident's logs from the last 7 days and takes the newest version
        |  3. looks for a Datadog incident whose "Cyberhaven Incident ID" (source_incident_id) matches
        v
Datadog Incident  created if none exists, updated if one does
```

The workflow needs a Datadog incident type with a set of Cyberhaven property fields. The setup script creates them for you.

## What is in this folder

| File | Purpose |
|---|---|
| `setup_datadog_incident_type.py` | Creates the **Cyberhaven Incident** incident type and its property fields in your Datadog org, then prints the incident type UUID. Safe to re-run. |
| `cyberhaven_create_update_incident.json` | The Datadog Workflow Automation workflow to import. Its `Create_incident` step contains the placeholder `REPLACE_WITH_INCIDENT_TYPE_UUID`, which you replace with the UUID from the script. |

The monitor ships with the Cyberhaven integration as the **[Cyberhaven] Incident created or updated** template.

## Prerequisites

- The Cyberhaven integration is installed and **Incident** logs are arriving. In the Log Explorer, `source:cyberhaven cyberhaven.logtype:cyberhaven-incidents` must return results. See the integration's setup guide, Step 2.
- **Incident Management** and **Workflow Automation** are available in your Datadog org.
- Python 3.8 or later on the machine that runs the script. It uses only the standard library.
- A Datadog **API key** and **application key**. The application key's owner needs the **Incident Settings Write** and **Incident Read** permissions, and the key must not be scoped without them.
- A Datadog user who can import and publish workflows. The workflow runs as the user who publishes it, so that user needs `logs_read_data`, `logs_read_index_data`, `incident_read` and `incident_write`.

## Setup

Do the steps in this order. Create the monitor last, so it can never alert before the workflow exists.

### 1. Get the files

Download or clone [Datadog/integrations-extras](https://github.com/Datadog/integrations-extras) and open the `cyberhaven/assets/incident-automation` folder.

### 2. Create the incident type and fields

Set your keys and your Datadog site. `DD_SITE` is the site your org is on, for example `datadoghq.com`, `datadoghq.eu`, `us3.datadoghq.com`, `us5.datadoghq.com`, `ap1.datadoghq.com` or `ddog-gov.com`.

```bash
export DD_API_KEY="<your API key>"
export DD_APP_KEY="<your application key>"
export DD_SITE="datadoghq.com"
```

Run the script:

```bash
python3 setup_datadog_incident_type.py
```

The script:

1. Creates the **Cyberhaven Incident** incident type (prefix `CH`), or reuses it if it exists.
2. Creates the 30 Cyberhaven property fields on it, skipping any that already exist.
3. Reads the fields back and confirms all 30 are present.
4. Prints the incident type UUID.

A successful run ends with `verified: all 30 fields are present` and `incident_type_uuid = <uuid>`. Copy the UUID for the next step. If the run fails, fix the cause and run it again. See [Troubleshooting](#troubleshooting).

### 3. Import the workflow

1. In Datadog, go to **Workflow Automation**, click **New Workflow**, then **Import from JSON**.
2. Select `cyberhaven_create_update_incident.json`.
3. Keep the handle `cyberhaven-create-update-incident`. The monitor's `@workflow-cyberhaven-create-update-incident` handle depends on it.
4. Open the **Create_incident** step and replace `REPLACE_WITH_INCIDENT_TYPE_UUID` in `incident_type_uuid` with the UUID the script printed.
5. Click **Publish**.

### 4. Create the monitor

1. In Datadog, go to **Monitors > Templates** and search for `Cyberhaven`.
2. Open **[Cyberhaven] Incident created or updated** and click **Create Monitor**.
3. Optionally add people or channels under **Notify your team**. The workflow handle is already in the monitor message.
4. Click **Create**.

When you create the monitor, it evaluates the last hour. It raises one alert for each Cyberhaven incident version logged in that hour, so the workflow runs once for each. This is expected and safe, because the workflow updates an existing Datadog incident instead of creating a duplicate.

### 5. Verify end to end

1. Create or update a Cyberhaven incident, or wait for the next one. For an update, change its status or add a note in the Cyberhaven console.
2. Within a few minutes, open the workflow in **Workflow Automation** and check its recent runs. A successful run ends at **Create_incident** or **Update_incident**.
3. In **Incidents**, find the Datadog incident. Its **Cyberhaven Incident ID** field matches the Cyberhaven incident, and its title reads `<policy> - <action> by <user>`.
4. Update the same Cyberhaven incident again. The existing Datadog incident updates and its **Last Change** field shows what changed. No second incident is created.

## What is created in Datadog

**Title:** `<policy name> - <action> by <user>`, at most 100 characters.

**Built-in fields**

| Datadog field | Value |
|---|---|
| Severity | From the policy severity: critical = SEV-1, high = SEV-2, medium = SEV-3, low = SEV-4, informational = SEV-5. Any other or missing value is UNKNOWN. |
| State | Cyberhaven `open` = active, `closed` = resolved. |
| Detection method | `monitor` |
| Summary | The Cyberhaven AI summary, action and outcome, status, timestamps and a link to the incident. |

**Cyberhaven property fields** (all text): Cyberhaven Incident ID (`source_incident_id`, the lookup key), Cyberhaven Incident URL, Tenant, Policy Name, Policy Severity, AI Severity, Created By, Dataset Name, Dataset Sensitivity, Risk Score, Blocked, User, User ID, Action, Hostname, Device Type, Sensor Kind, Client IP, Data Size (bytes), Warning Status, Event Time, Trigger Time, Resolution Time, Close Reason, Close Note, Cyberhaven Status, AI Summary, Policy ID, Dataset ID, and **Last Change**.

**Last Change** compares the newest version of the incident with the previous one, ignoring timestamps, and lists each attribute that changed (`key: old -> new`). The first version reads `First version seen`.

When the incident is created, a markdown note with every attribute of the Cyberhaven log is added to it.

## Behavior and limits

- **Updates overwrite.** Each update replaces the title, severity, state and all Cyberhaven fields with Cyberhaven's latest values, so a manual edit to those in Datadog is lost on the next update. Fields you add yourself, and other parts of the incident, are not touched.
- **The note is written once**, when the incident is created. It is not refreshed on updates. The Summary and Last Change fields are.
- **Cleared values are not cleared.** Empty values are not sent, because the Incidents API rejects them. If a value becomes empty in Cyberhaven (for example a close note after a reopen), the old value stays in Datadog. The Cyberhaven Status field always shows the current state.
- **Late logs.** The monitor evaluates the last hour, so an incident log that reaches Datadog up to an hour after its timestamp is still picked up. Datadog does not ingest logs timestamped more than 18 hours in the past. See the integration README.
- **Version history.** Last Change compares against earlier versions from the last 7 days. An older incident shows `First version seen`.
- **Rare duplicates.** If Cyberhaven sends an incident's creation and first update within seconds of each other, they run as separate workflow runs and both may create an incident. Search for the same `source_incident_id` to find and merge them.
- **Failures are visible.** Every failure ends the workflow run with an error naming the incident, so nothing is skipped silently. Lookups, creates and updates retry three times, 10 seconds apart.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Script: `not authorized` | The application key's owner lacks **Incident Settings Write** or **Incident Read**, the key is scoped without them, or `DD_SITE` is not the site your org is on. |
| Script: `N of 30 fields are missing` | One or more field creations failed. Read the `could not create field` lines above it, fix the cause and re-run. Existing fields are skipped. |
| Workflow run fails at **Log_lookup_failed** | The Logs search failed three times. Check that the workflow's publishing user has `logs_read_data` and `logs_read_index_data`. |
| Workflow run fails at **No_incident_logs_found** | No incident log was found for that id in the last 7 days. Check that the monitor groups by `@cyberhaven.incident.id`, that an index exclusion filter is not dropping `source:cyberhaven cyberhaven.logtype:cyberhaven-incidents`, and that the Cyberhaven incidents export is still running. |
| Workflow run fails at **Incident_lookup_failed** | The Incidents search failed three times. Check that the publishing user has `incident_read`. Nothing was created, to avoid a duplicate. |
| Workflow run fails at **Create_incident_failed** | Check that `incident_type_uuid` is your incident type UUID and not `REPLACE_WITH_INCIDENT_TYPE_UUID`, that all 30 fields exist, and that the publishing user has `incident_write`. |
| Workflow run fails at **Update_incident_failed** | Check that the publishing user has `incident_write` and that the Datadog incident was not deleted. |
| Monitor alerts but the workflow never runs | Confirm the workflow is **published** with the handle `cyberhaven-create-update-incident`. Alerts that fired before it was published do not re-fire. |
| No incidents appear and no alerts fire | Confirm the monitor exists and Incident logs are arriving (see Prerequisites). |

## Remove

1. In **Monitors**, delete the **[Cyberhaven] Incident created or updated** monitor.
2. In **Workflow Automation**, delete or disable the `cyberhaven-create-update-incident` workflow.
3. Optional: in **Incidents > Settings**, delete the **Cyberhaven Incident** incident type, only if you no longer need the Datadog incidents this workflow created.
