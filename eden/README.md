# Agent Check: Eden

## Overview

This integration ships Eden-MDBS metrics into Datadog so you can monitor Eden
alongside the rest of your stack. Two collection paths are
supported and can be used together:

- **Agent check (recommended)** -- the Datadog Agent polls Eden's
  `/api/v1/analytics/telemetry` API every minute and submits metrics under the
  `eden.*`, and related namespaces.
- **DogStatsD direct export (self-host only)** -- Eden pushes metrics straight
  to the Agent's DogStatsD listener every 10 seconds for lower-latency counters,
  gauges, and distributions. Requires the Agent to be reachable from the Eden
  node.

Pre-built Eden dashboards are installed automatically when you enable the tile
in Datadog.

## Setup

### Prerequisites

- Datadog Agent **v6.10.0 or later**.
- An Eden organization. SaaS customers already have one; self-host customers
  need a running Eden deployment reachable from the Agent.
- A Datadog account with permission to install integration tiles.
- For self-host: network connectivity from the Datadog Agent to your Eden API.

### Step 1 -- Enable the Eden tile in Datadog

1. In Datadog, go to **Integrations -> Marketplace** and search for **Eden**.
2. Click **Install** on the Eden tile. This:
   - Adds Eden to your organization's installed integrations
   - Provisions the Eden dashboards
   - Enables the `eden.api.can_connect` service check
   - Registers Eden metric metadata for autocomplete

The tile install does **not** prompt for credentials. The Datadog Agent that
runs on your hosts is configured separately in steps 2-4.

### Step 2 -- Create an Eden robot for the Agent

The Agent authenticates to Eden using a long-lived **robot API key**. Robots are
machine accounts scoped to a single organization and a fixed permission set.

1. In the Eden Dashboard, switch to the organization whose telemetry you want
   to ship to Datadog.
2. Open the **Robots** page (under IAM / Access).
3. Click **Create Robot** and fill in:
   - **Username:** `datadog-agent` (or any descriptive name)
   - **Description:** _Datadog Agent -- telemetry export_
   - **Permissions:** check **Read** under control plane permissions. Read is
     all the integration needs.
4. After creation, the Eden Dashboard shows the robot's `api_key` **once**.
   Copy it now -- you cannot retrieve it later. If lost, use the **Rotate Key**
   action on the robot to issue a new one.

Note your **Org ID** (visible in the Dashboard under organization settings) --
the Agent needs it on every login request.

> **Tip:** If you operate multiple Eden organizations, create one robot per org
> and add a separate instance entry in `eden.yaml` for each.

### Step 3 -- Install the integration package on each Datadog Agent host

On every host or container running the Datadog Agent that should collect Eden
metrics:

```shell
sudo -u dd-agent datadog-agent integration install -t datadog-eden==<VERSION>
```

(Use `sudo` without `-u dd-agent` on macOS; on Windows, run an elevated
PowerShell with the path to `agent.exe`. See Datadog's
[Community and Marketplace Integrations][cmi] guide for full per-platform
commands.)

[cmi]: https://docs.datadoghq.com/getting_started/integrations/#community-and-marketplace-integrations

### Step 4 -- Configure the Agent

Edit `eden.d/eden.yaml` inside the Agent's `conf.d/` directory
(typically `/etc/datadog-agent/conf.d/eden.d/eden.yaml` on Linux):

```yaml
init_config:

instances:
  - url: https://api.eden.example.com # Eden API base URL
    org_id: AcmeCorp # or use org_uuid: <UUID>
    robot_username: datadog-agent
    robot_api_key: eden_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    min_collection_interval: 60 # seconds between checks
    tags:
      - env:prod # any global tags you want on every Eden metric
```

Then restart the Agent so it picks up the new instance:

```shell
sudo systemctl restart datadog-agent
```

#### Configuration options reference

| Option                             | Required | Default      | Description                                                                                                                                                                                                    |
| ---------------------------------- | -------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`                              | yes      | --            | Eden API base URL. Use `https://api.eden.example.com` for SaaS or your internal URL for self-host.                                                                                                             |
| `org_id` _or_ `org_uuid`           | yes      | --            | Eden organization scope for login. Provide whichever you have on hand.                                                                                                                                         |
| `robot_username` + `robot_api_key` | yes      | --            | Robot credentials from Step 2.                                                                                                                                                                                 |
| `metric_groups`                    | no       | _all groups_ | Restrict export to specific groups (e.g. `[proxy, workload]`) to control custom metric volume. Valid values: `analytics`, `eden`, `iam`, `endpoint`, `metadata`, `migration`, `proxy`, `snapshot`, `workload`. |
| `range_seconds`                    | no       | `300`        | Backfill window on first run, also a safety bound on each subsequent poll.                                                                                                                                     |
| `limit`                            | no       | `5000`       | Maximum rows per group per HTTP request. The check paginates automatically; you rarely need to change this.                                                                                                    |
| `token_refresh_window_seconds`     | no       | `120`        | Refresh cached JWTs this many seconds before expiry.                                                                                                                                                           |
| `min_collection_interval`          | no       | `60`         | How often the Agent runs the check.                                                                                                                                                                            |
| `tags`                             | no       | _none_       | Global tags appended to every metric and service check this instance emits.                                                                                                                                    |

### Step 5 -- Validate

Run on the Agent host:

```shell
sudo datadog-agent status | sed -n '/^=*/,/^=*/p' | grep -A 8 'eden'
```

You should see something like:

```
eden (0.1.0)
------------
  Instance ID: eden:... [OK]
  Total Runs: 7
  Metric Samples: Last Run: 89, Total: 612
  Service Checks: Last Run: 1, Total: 7
  Last Successful Execution Date: ...
```

In Datadog itself:

- **Metrics -> Summary**, filter by `eden_service:eden` -- you should see `eden.*`,
  `eden.proxy.*`, `eden.workload.*` metrics with non-zero counts.
- **Monitors -> New Monitor**, type "Service Check", search
  `eden.api.can_connect` -- the check appears once telemetry has flowed.
- **Dashboards** -- Eden dashboards should populate within a couple of minutes
  for the metric groups your deployment emits.

### (Optional) DogStatsD direct export -- self-host only

For self-host customers who run the Datadog Agent on the same host (or pod) as
Eden, you can additionally have Eden push metrics straight to the Agent's
DogStatsD listener every 10 seconds. This complements the Agent check by
delivering live counters and native distributions for percentile queries.

1. Make sure the Datadog Agent is configured to receive DogStatsD UDP traffic
   (default port `8125`). If the Agent runs in Docker, bind `8125/udp` and set
   `DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true`.
2. On the Eden node, set the listener address before starting eden-service:

   ```shell
   export EDEN_DOGSTATSD_ENDPOINT=127.0.0.1:8125
   ```

   Use the Agent's reachable address if it's not on `127.0.0.1` (e.g.
   `dd-agent:8125` if you're on a Docker network with the Agent named
   `dd-agent`).

3. Restart eden-service.

Eden will continue to write metrics to ClickHouse for the Agent check
regardless -- the two paths are independent.

## Multi-organization deployments

If you operate Eden across multiple organizations (for example, separate
`AcmeCorp` and `AcmeCorpEU` orgs), create one robot per org and list each as a
separate instance:

```yaml
instances:
  - url: https://api.eden.example.com
    org_id: AcmeCorp
    robot_username: datadog-agent
    robot_api_key: <EDEN_ROBOT_API_KEY_US>
    tags: [env:prod, region:us]

  - url: https://api.eden.example.com
    org_id: AcmeCorpEU
    robot_username: datadog-agent
    robot_api_key: <EDEN_ROBOT_API_KEY_EU>
    tags: [env:prod, region:eu]
```

Each instance gets its own JWT cache and cursor; data from different orgs is
tagged separately so you can build per-org dashboards by filtering on
`org_uuid`.

## Troubleshooting

### Service check is `CRITICAL`

`eden.api.can_connect` reports `CRITICAL` whenever the Agent fails to reach the
Eden API or login fails.

- Run the check in the foreground for a verbose error message:

  ```shell
  sudo -u dd-agent datadog-agent check eden -l debug
  ```

- Common causes:
  - Wrong `url` (mistyped scheme/host) or unreachable DNS from the Agent host.
  - Wrong `org_id` / `org_uuid`. Eden returns `400` when the organization
    header doesn't match a known org.
  - Robot key was rotated or revoked, or the robot lost `control: read`.
  - TLS interception in the network path (corp proxy without trusted CA).

### "`robot_username` and `robot_api_key` are required in eden.yaml"

The instance is missing one or both of the robot credentials. Create a robot
in the Eden Dashboard (Step 2) and paste both values into `eden.yaml`.

### Metric volume looks high

The check exports every Eden metric group by default, which on busy
deployments can produce a few hundred custom metrics per host. Trim it down
with `metric_groups`:

```yaml
metric_groups:
  - eden
  - proxy
  - workload
```

### "401 Unauthorized" repeating in the Agent log

The robot's API key is invalid or the robot is in a different organization
than `org_id`. Re-create the robot, double-check the org, and rotate the key.
The Agent automatically retries with a fresh JWT on a single 401, but
persistent 401s indicate a misconfiguration.

### Metrics are present in DogStatsD but not in the Agent check

Both paths use the same Eden source data, but the Agent check polls
ClickHouse-backed history while DogStatsD pushes live samples. If a metric
appears in DogStatsD but not in the Agent check, ensure ClickHouse telemetry
sync is enabled on the Eden side (look for `ClickHouse telemetry sync enabled`
in eden-service logs).

## Data Collected

### Metrics

The integration emits ~50-150 metrics depending on which groups are enabled
and which features your Eden deployment uses. See `metadata.csv` in the
package for the authoritative list. Highlights:

- **`eden.*`** -- request lifecycle, cache, auth, RBAC sync lag.
- **`eden.endpoint.*`** -- per-endpoint request counts and durations.
- **`eden.proxy.*`** -- proxy lane pool and shard metrics.
- **`eden.workload.*`** -- workload telemetry per Redis endpoint.
- **`eden.analytics.*`** -- analytics pipeline sampling and burst metrics.
- **`eden.migration.*`**, **`eden.snapshot.*`** -- migration and snapshot subsystems.

Distribution metrics are exported as three series: `<name>.count`,
`<name>.sum`, and `<name>.avg`. If you also enable DogStatsD direct export,
you get the same metric as a native Datadog distribution suitable for
percentile queries.

> **Known divergence with DogStatsD direct export.** The Agent check forces
> every metric under the `eden.*` namespace because the integration tile is
> registered with that prefix in Datadog's marketplace. Eden's DogStatsD
> exporter (configured by `EDEN_DOGSTATSD_ENDPOINT`) currently emits some
> metrics under top-level namespaces such as `proxy.*`, `workload.*`, and
> `analytics.*` -- so the same underlying metric can appear under two names
> if both paths are enabled. The two should be aligned: either rename the
> DogStatsD-side metrics to also start with `eden.`, or relax the Agent
> check's `_metric_name` to drop the forced prefix once the tile prefix
> requirement is loosened.

### Service Checks

| Name                   | Description                                                                                                                                                                            |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `eden.api.can_connect` | Returns `OK` when the Agent reaches the Eden export API and successfully fetches a page of telemetry; `CRITICAL` otherwise. Tags include any global `tags` configured on the instance. |
