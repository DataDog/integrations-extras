# Huntress

## Overview

[Huntress](https://www.huntress.com/) is a managed security platform providing endpoint detection and response (EDR), antivirus, security awareness training, and a Managed SIEM product that continuously collects and analyzes endpoint telemetry.

This integration polls the Huntress Managed SIEM API using ES|QL queries and forwards all security events to Datadog as logs. Each collection run:

1. Loads a checkpoint — the timestamp of the last successful collection
2. Executes a configurable ES|QL query for the elapsed time window
3. Paginates through all result pages
4. Optionally enriches each log with Huntress organization metadata (org name, key, account ID)
5. Forwards logs to Datadog preserving all Elastic Common Schema (ECS) field names
6. Advances the checkpoint only after all pages are successfully sent

This integration is designed for managed security providers (MSPs) and enterprise teams who want to correlate Huntress threat detections alongside infrastructure and application telemetry in Datadog.

## Setup

### Prerequisites

- Datadog Agent 7.x or later
- A Huntress account with the Managed SIEM feature enabled
- Huntress API credentials (public API key + secret key) from the Huntress Partner Portal under **Settings > API Credentials**

### Installation

Install the integration package from the Agent:

```bash
datadog-agent integration install -t datadog-huntress==1.0.0
```

### Configuration

1. Create the configuration file at `/etc/datadog-agent/conf.d/huntress.yaml` (Linux/macOS) or `C:\ProgramData\Datadog\conf.d\huntress.yaml` (Windows). A fully-annotated example is at `datadog_checks/huntress/data/conf.yaml.example`.

2. Edit `huntress.yaml` with your credentials:

   ```yaml
   init_config: {}

   instances:
     - huntress_api_key: "<your_public_api_key>"
       huntress_secret_key: "<your_secret_api_key>"
       esql_query: "FROM logs"
       tags:
         - "source:huntress"
         - "service:huntress-siem"
         - "env:production"
   ```

3. Restart the Agent:

   ```bash
   # Linux (systemd)
   sudo systemctl restart datadog-agent

   # macOS
   sudo launchctl stop com.datadoghq.agent && sudo launchctl start com.datadoghq.agent
   ```

4. Verify the check:

   ```bash
   sudo datadog-agent check huntress
   ```

   Logs appear in Datadog Log Explorer filtered by `source:huntress` within one collection interval (default: 15 minutes).

### Multiple Huntress accounts

Add additional blocks under `instances:` — each runs independently with its own checkpoint, org metadata cache, and metrics:

```yaml
instances:
  - huntress_api_key: "<account1_key>"
    huntress_secret_key: "<account1_secret>"
    esql_query: "FROM logs"
    tags: ["source:huntress", "env:production"]

  - huntress_api_key: "<account2_key>"
    huntress_secret_key: "<account2_secret>"
    esql_query: "FROM logs"
    tags: ["source:huntress", "env:staging"]
```

### Configuration reference

| Field                     | Required | Default                   | Description                               |
| ------------------------- | -------- | ------------------------- | ----------------------------------------- |
| `huntress_api_key`        | Yes      | —                         | Huntress public API key                   |
| `huntress_secret_key`     | Yes      | —                         | Huntress secret API key                   |
| `esql_query`              | Yes      | —                         | ES\|QL query; must begin with `FROM logs` |
| `enrich_with_org_tags`    | No       | `true`                    | Fetch and attach org metadata as log tags |
| `org_cache_ttl_seconds`   | No       | `3600`                    | How long to cache org metadata (seconds)  |
| `min_collection_interval` | No       | `900`                     | Seconds between runs (minimum 60)         |
| `max_pages_per_run`       | No       | `100`                     | Page cap per run (~20,000 logs maximum)   |
| `huntress_base_url`       | No       | `https://api.huntress.io` | Override for sandbox environments         |
| `tags`                    | No       | `[]`                      | Extra tags on every forwarded log         |

## Data Collected

### Logs

All logs collected from the Huntress Managed SIEM API are forwarded to Datadog with:

- `ddsource: huntress` — enables automatic log pipeline processing
- ECS field names preserved as top-level log attributes (for example, `event.category`, `host.hostname`, `user.name`)
- Organization metadata tags when `enrich_with_org_tags: true` (for example, `huntress_org_name`, `huntress_org_key`, `huntress_account_id`)

### Metrics

| Metric                               | Type  | Description                                             |
| ------------------------------------ | ----- | ------------------------------------------------------- |
| `huntress.siem.logs_collected`       | Gauge | Log events collected per run                            |
| `huntress.siem.pages_fetched`        | Gauge | API pages fetched per run                               |
| `huntress.siem.run_duration_seconds` | Gauge | Wall time of the collection run                         |
| `huntress.siem.errors`               | Count | Errors by type (`error_type` tag)                       |
| `huntress.siem.api_call_limit`       | Gauge | Total API requests allowed per minute (from Huntress)   |
| `huntress.siem.api_call_remaining`   | Gauge | API requests remaining in the current minute            |

See [metadata.csv][1] for a full list of metrics.

### Events

The Huntress integration does not emit Datadog events.

### Service Checks

**`huntress.siem.check_status`**  
Returns `CRITICAL` if the collection run fails for any reason; `OK` otherwise.

## Troubleshooting

**No logs in Datadog after first run**

- Run `sudo datadog-agent check huntress` and inspect the output
- Verify the API key pair is valid by checking the Huntress Partner Portal
- Confirm the Managed SIEM feature is enabled on the account
- Check that `esql_query` begins with `FROM logs`

**`huntress.siem.errors` count is increasing**

Inspect the `error_type` tag to identify the root cause:

| `error_type`       | Cause                              | Resolution                                                   |
| ------------------ | ---------------------------------- | ------------------------------------------------------------ |
| `auth_failure`     | Invalid or rotated API credentials | Update `huntress_api_key` / `huntress_secret_key`            |
| `timeout`          | ES\|QL query too broad             | Add a `KEEP` or `WHERE` clause to the query                  |
| `invalid_query`    | Malformed ES\|QL                   | Fix the `esql_query` value                                   |
| `server_error`     | Transient Huntress API error       | Check [Huntress status page](https://status.huntress.com)    |
| `connection_error` | Network issue                      | Verify connectivity from the Agent host to `api.huntress.io` |
| `run_failure`      | Unexpected error during collection | Check Agent logs for the full stack trace                    |

**`huntress.siem.api_call_remaining` is very low or zero**

The Huntress API allows 60 requests per minute. The integration logs a warning when fewer than 10 requests remain in a given minute. If this happens regularly, reduce `max_pages_per_run` or increase `min_collection_interval` to spread out collection runs.

**Duplicate logs after Agent restart**

This is expected on the first restart after a failed run — the checkpoint is only advanced when all pages are successfully sent. Subsequent runs resume from the last successful checkpoint.

Need help? Contact [Datadog support][2].

## Support

For questions and support, [contact Datadog support][2].

[1]: https://github.com/DataDog/integrations-extras/blob/master/huntress/metadata.csv
[2]: https://docs.datadoghq.com/help/
