# Cyberhaven incidents in Datadog Incident Management

Create and update a Datadog incident for every Cyberhaven incident, using the Incident logs the Cyberhaven integration already streams into Datadog.

This is optional. The Cyberhaven integration works without it.

## How it works

The **[Cyberhaven] Incident created or updated** monitor alerts once per incident version (grouped by `@cyberhaven.incident.id` and `@cyberhaven.incident.last_modified`) and triggers the `cyberhaven-create-update-incident` workflow. The workflow loads the newest log for that incident from the last 7 days, then looks for a Datadog incident whose **Cyberhaven Incident ID** (`source_incident_id`) matches. It updates that incident, or creates one if none exists.

## Files

| File | Purpose |
|---|---|
| `setup_datadog_incident_type.py` | Creates the **Cyberhaven Incident** incident type and its 30 property fields, then prints the incident type UUID. Safe to re-run. |
| `cyberhaven_create_update_incident.json` | The Workflow Automation workflow to import. Its `Create_incident` step contains the placeholder `REPLACE_WITH_INCIDENT_TYPE_UUID`. |

The monitor ships with the Cyberhaven integration as a monitor template.

## Prerequisites

- The Cyberhaven integration is installed and Incident logs are arriving: `source:cyberhaven cyberhaven.logtype:cyberhaven-incidents` returns results in the Log Explorer.
- **Incident Management** and **Workflow Automation** are available in your Datadog org.
- Python 3.8 or later. The script uses only the standard library.
- A Datadog API key and application key. The application key's owner needs the **Incident Settings Write** and **Incident Read** permissions.
- A Datadog user who can import and publish workflows. The workflow runs as the user who publishes it, so that user needs `logs_read_data`, `logs_read_index_data`, `incident_read` and `incident_write`.

## Setup

Follow the steps in order. Create the monitor last, so it cannot alert before the workflow exists.

### 1. Create the incident type and fields

Download or clone [partner-integration-artifacts](https://github.com/CyberhavenInc/partner-integration-artifacts), open the `datadog/incident-automation` folder, and run:

```bash
export DD_API_KEY="<your API key>"
export DD_APP_KEY="<your application key>"
export DD_SITE="datadoghq.com"   # the site your org is on, for example datadoghq.eu
python3 setup_datadog_incident_type.py
```

A successful run ends with `verified: all 30 fields are present` and `incident_type_uuid = <uuid>`. Copy the UUID. If the run fails, fix the cause and run it again. See [Troubleshooting](#troubleshooting).

### 2. Add the UUID to the workflow file

Open `cyberhaven_create_update_incident.json` in a text editor and replace `REPLACE_WITH_INCIDENT_TYPE_UUID` with the UUID from step 1. It appears once, as the `incident_type_uuid` value in the `Create_incident` step. Save the file.

### 3. Import the workflow

1. In Datadog, go to **Workflow Automation**, click **New Workflow** > **Import workflow**, and select `cyberhaven_create_update_incident.json`.
2. Click **Yes, Replace and Save**.

### 4. Create the monitor

1. In Datadog, go to **Monitors > Browse Templates** and search for `Cyberhaven`.
2. Open **[Cyberhaven] Incident created or updated**.
3. Under **Notify your team**, keep the `@workflow-cyberhaven-create-update-incident` handle, optionally add people or channels to alert (for example, `@your-team-email` or `@slack-your-channel`), then click **Create and Publish**.

## What is created in Datadog

- **Title:** `<policy> - <action> by <user>`.
- **Severity:** from the policy severity: critical = SEV-1, high = SEV-2, medium = SEV-3, low = SEV-4, informational = SEV-5. Any other value is UNKNOWN.
- **State:** Cyberhaven `open` = active, `closed` = resolved.
- **Property fields:** the Cyberhaven log attributes, including **Cyberhaven Incident ID** (the lookup key), policy, dataset, user, action and status, plus **Last Change**, which lists what changed since the previous version as `key: old -> new`.
- **Note:** on creation, a note with every attribute of the Cyberhaven log.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Script: `not authorized` | Check that the application key's owner has **Incident Settings Write** and **Incident Read**, and that `DD_SITE` is your org's site. |
| Workflow run fails | Open the failed run to see the step that failed. Check that the publishing user has the permissions listed in Prerequisites, that no index exclusion filter drops the Cyberhaven incident logs, and that the UUID in step 2 is not the placeholder. |
| Monitor alerts but the workflow never runs | Confirm the workflow is published with the handle `cyberhaven-create-update-incident`. Alerts that fired earlier do not re-fire. |
| No alerts fire | Confirm the monitor exists and Incident logs are arriving. |
