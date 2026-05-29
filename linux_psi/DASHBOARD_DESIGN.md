# Dashboard design notes

This document explains the *intent* behind the shipped `Linux PSI Overview` dashboard, what it deliberately does not yet do, and a planned set of v1.1 additions that turn raw PSI metrics into operational insight. It exists so a future maintainer (or the original author six months later) can extend the dashboard without re-deriving the design.

The shipped JSON lives at `assets/dashboards/linux_psi_overview.json`. This note is the *why*; the JSON is the *what*.

## 1. Design philosophy

The shipped v1 dashboard is the **minimum viable layer**: every metric has a place, every resource is represented, and a first-time visitor can read the "About PSI" intro widget and understand what they are looking at. It is not yet a dashboard that answers operational questions on its own.

The dashboard that answers questions, the v1.1 design described below, is **organized by the question an operator wants answered, not by the metric being shown**. This is the principal design shift: instead of "here is `cpu.some.avg60`, here is `memory.some.avg60`, here is `io.some.avg60`", the v1.1 panels are "is anything wedging this host right now?", "is this host right-sized?", "what is the trend?", and so on.

This matters because PSI's value is comparative and compositional. A single PSI number in isolation is rarely actionable; a PSI number in the context of fleet behavior, workload deploys, or capacity envelopes is.

## 2. Shipped dashboard layout

The shipped dashboard has **30 widgets across 7 collapsible groups**, plus 5 template variables (`host`, `env`, `service`, `cgroup_path`, `cgroup_root`). Designed to read top-to-bottom and answer increasingly-detailed questions:

| Group | Color | Purpose | Default state |
|---|---|---|---|
| About header | blue | One-paragraph orientation + legend | Always visible |
| Status: is anything on fire? | pink | 4 KPI tiles (worst memory full / CPU some / IO some / composite) with red/yellow/green conditional formatting | Always visible |
| Live trends: where is the wedge? | blue | Stacked 3-resource chart + per-resource panels + composite-by-host | Always visible |
| Fleet view | purple | Top-N hosts by each pressure + cumulative-stall ranking + distribution histogram | Always visible |
| Per-host investigation | green | Some-vs-full overlays + stall rate per second; uses `$host` template variable | Collapsible |
| Per-cgroup view | yellow | Top cgroups by CPU/memory + per-cgroup timeseries; populated only when `cgroup_roots` is configured | Collapsible |
| Capacity & trends | orange | Week-over-week comparison + pressure-budget leaderboard | Collapsible |
| Reference - raw timeseries | gray | All-windows (avg10/60/300) per-resource for custom-query authoring | Collapsible |

The first three groups answer the on-call SRE's question ("what's wrong now?") in under 5 seconds. The investigation and cgroup groups answer the performance engineer's question ("which workload caused this?"). The capacity group answers the planner's question ("are we sized right?").

Each widget's purpose is stated in its title - the dashboard is self-documenting at the widget level, not just at the design-doc level.

## 3. Original v1.1 design - six question-driven panels (now shipped)

The panels listed in this section were the original v1.1 design. They have all shipped in the dashboard described in section 2 above. Kept here as the rationale-record so a future maintainer understands why each panel exists.

The v1.1 dashboard adds the following widgets, grouped into a `Diagnostic` tab (panels A and B) and a `Capacity` tab (panels C through F), with the existing v1 widgets retained in a third `Reference` tab. The tabbed layout means on-call uses tab one, capacity planning uses tab two, and the raw metric inspector lives in tab three.

### Panel A - Stacked three-resource view

> **Question:** Right now, what dimension is wedging this host?

A single timeseries panel with three lines: `psi.system.pressure.cpu.some.avg60`, `psi.system.pressure.memory.some.avg60`, `psi.system.pressure.io.some.avg60`. Scoped to a single host via the existing `$host` template variable.

The line that spikes during an incident identifies the contended resource in one glance. Replaces three separate v1 panels for the most common diagnostic use case.

**Datadog functions used:**
- `default_zero()` on each line so a briefly-absent resource (e.g., cgroup-restricted I/O) does not break the chart
- `anomalies(query, 'agile', 3)` overlay band on each line so the operator sees not just current value but how unusual it is for this host

A 15% spike that is anomalous for one host and routine for another tells two very different stories; the anomaly band makes that visible.

### Panel B - "Severe contention now" indicator

> **Question:** Is anything page-worthy at this exact moment?

A query-value widget with conditional formatting. The query takes the top host across all three `full.avg10` metrics, filtered to values above 5%. If empty, the widget shows "All clear" in green. If non-empty, it shows the offending host and resource in red.

`some` pressure being high is interesting; `full` pressure being high means *every task* on the host is stalled, which is much harder to recover from gracefully and warrants a page even at low values.

**Datadog functions used:**
- `top(query, 1, 'mean', 'desc')`
- Conditional formatting on the value range to color-code the cell

### Panel C - Pressure-budget heatmap

> **Question:** Which hosts are sizing-stressed over the last week?

A heatmap or top-list where each row is a host and the value is "% of the last 7 days during which `memory.some.avg300` exceeded 5%". Hosts with high pressure-budget consumed are the candidates for the next scale-up round, regardless of what their utilization numbers look like.

**Datadog functions used:**
- `count_nonzero(psi.system.pressure.memory.some.avg300 > 5, 'last_7d')` or equivalent via Datadog's threshold-aggregation widgets
- Rolled up to per-host with `by {host}`

The same pattern can be repeated for CPU and I/O as separate widgets, or three resources can be combined via a composite score (see section 4).

### Panel D - Pressure vs utilization quadrant

> **Question:** Is this host right-sized?

A scatter widget with utilization on the x-axis (`system.cpu.usage` averaged over the last hour) and pressure on the y-axis (`psi.system.pressure.cpu.some.avg300`). Each dot is one host. The four quadrants tell different stories:

- Low utilization + low pressure: oversized, money on the table
- High utilization + low pressure: right-sized, productive
- High utilization + high pressure: undersized, scale up
- Low utilization + high pressure: noisy neighbor or workload mismatch

This single chart drives a quarterly capacity-review conversation more efficiently than any number of timeseries.

### Panel E - Week-over-week pressure delta

> **Question:** Is pressure trending up?

A timeseries showing `psi.system.pressure.memory.some.avg60 - week_before(psi.system.pressure.memory.some.avg60)`. Positive bars mean pressure is worse than last week at the same time of day; negative bars mean it has improved.

Overlay deployment events (from a CI integration that emits to Datadog Events) on the x-axis. When a positive delta starts shortly after a deploy marker, you have a direct visual link from a release to a regression.

**Datadog functions used:**
- `week_before()` (or `hour_before()`, `day_before()`) for period-over-period comparison
- Event overlay widget setting (any integration emitting deploy events is fine)
- Optional `ewma_3()` smoothing on the delta line to make the trend readable

### Panel F - Pressure SLO board

> **Question:** Are we meeting our pressure objective?

Datadog has a first-class SLO widget. Define an SLO of the form "`memory.full.avg300 < 5%` over a rolling 30-day window" with a 99.5% objective. The widget shows current attainment, error budget remaining, and burn rate.

This turns pressure into a formal contract. When the error budget burns faster than the 30-day allocation, you have a quantitative argument for the capacity-expansion meeting, not "the dashboard looks bad lately."

**Datadog feature used:**
- Native SLO definition with a metric-query backing
- The SLO widget on the dashboard
- Optional alert on the burn rate exceeding 2x expected pace

## 4. The composite pressure score

A widget that shipped in v1 would have made the dashboard better even on its own: a **single per-host composite score** computed at query time:

```
composite_pressure = 0.4 * cpu.some.avg60
                   + 0.4 * memory.some.avg60
                   + 0.2 * io.some.avg60
```

The weighting reflects empirical experience: memory and CPU pressure are most often the binding constraint on user-visible latency; I/O matters less in most cloud-native workloads because the storage layer is already abstracted. These weights are debatable and should be tunable; a `template_variable` for the weight ratio would let teams adjust.

Render this as a heatmap widget with hosts on the y-axis and time on the x-axis, colored by composite score. The operator scans the heatmap, sees one or two hosts/hours that are bright red, and drills in. This is the single highest-density visualization PSI data supports.

The composite is **not a real emitted metric**. It is a formula computed in the widget query. This means it costs no extra storage, no extra cardinality, and any user can tune the weighting locally without changing the integration's emitted data.

## 5. What this design deliberately does not include

A few candidates I considered and ruled out:

| Candidate | Why ruled out |
|---|---|
| Per-process PSI panels | PSI is system-wide; we do not have per-process data. The "noisy neighbor" question is better answered by overlaying k8s/container metrics on the system-wide PSI panels. |
| ML-based anomaly detection on the `total` counter | The `derivative()` of a monotonic counter is conceptually identical to the `avg10`/`avg60` gauges PSI already exposes. ML adds complexity without insight here. |
| A "pressure forecast" panel | `forecast()` exists in Datadog and works on PSI metrics, but pressure forecasts have low predictive value on horizons longer than a few days because most pressure events are workload-driven, not workload-independent trends. Better to alert on the *current* week-over-week delta and let the operator interpret. |
| Per-cgroup PSI panels | The cgroup PSI data IS collected by the check as of v1.1 (opt-in via `cgroup_roots`). A v1.2 dashboard pass should add per-cgroup breakdowns of the panels above, grouped by `cgroup_path` or by the Agent tagger's enriched dimensions (`kube_namespace`, `kube_deployment`, `container_name`). Highest-value panels for the per-cgroup view: a heatmap of `psi.system.pressure.cgroup.memory.some.avg60` by `cgroup_path`, and a top-list of cgroups by `cgroup.cpu.some.avg300` over the last hour - this is the canonical "which workload is stressing this host?" question. |

## 6. v1.2 roadmap - panels worth adding next

Now that the v1.1 panels are shipped, the next round of improvements should target the things real on-call use will reveal as missing. Likely candidates in priority order:

1. **Pressure-vs-utilization scatter (Panel D from the original design)** - still not shipped because the scatter widget needs `system.cpu.usage` from the host integration to cross-reference. Worth adding once we confirm typical Datadog accounts running this integration also run the host check.
2. **Anomaly bands on the live charts** - `anomalies(query, 'agile', 3)` overlays on the per-resource panels in the Live Trends group. Lets the on-call see whether the current value is "high but normal for this host" vs "actually anomalous." Implementation note: needs at least 24 hours of historical data to be meaningful.
3. **SLO widget** - requires defining the SLO in Datadog first (a `psi.system.pressure.memory.full.avg300 < 5%` over 30d objective at 99.5%). Once defined, embed the SLO widget on the Capacity tab.
4. **Per-deploy correlation overlay** - event markers from a CI integration overlaid on the week-over-week panels. Requires the user to have a deploy-events source. Document as "drop your deploy events here" rather than hardcoding.
5. **Forecast** - `forecast()` on the cumulative stall rate, projecting 14 days. Useful for capacity reviews; not useful for on-call.

Each is independently shippable. Open a PR to integrations-extras for each one separately - small, reviewable, easy to roll back.

## 7. Validating the additions

Before merging any panel into `assets/dashboards/linux_psi_overview.json`:

1. **Import the proposed JSON into a Datadog account** that has at least a week of real PSI data flowing through it. Confirm every widget renders without "No data" errors.
2. **Sanity-check the queries on a host with known recent contention** (e.g., one where you intentionally ran a memory-heavy workload). Each panel should highlight the right host or time window.
3. **Test the SLO widget** by deliberately setting a tight threshold and confirming the error budget burns visibly. Then relax the threshold to a realistic value for production.
4. **Read the dashboard alongside another integration the user already has** (Postgres, vLLM, the OS check). Are the time axes synchronized? Do the host tag values match? Cross-integration consistency is what makes a dashboard feel like part of a system rather than a stray report.

A v1.1 PR that ships all six panels in one go is a large change to review. Smaller PRs, one or two panels at a time, each tied to a real operational use case in the PR description, will move through review faster and are more likely to survive a reviewer's "do we really need this?" question.

## 8. References

- [Datadog timeseries widget docs](https://docs.datadoghq.com/dashboards/widgets/timeseries/)
- [`anomalies` function](https://docs.datadoghq.com/dashboards/functions/algorithms/)
- [`forecast` function](https://docs.datadoghq.com/dashboards/functions/algorithms/#forecasts)
- [Period-over-period functions (`week_before`, `day_before`, `hour_before`)](https://docs.datadoghq.com/dashboards/functions/timeshift/)
- [SLO widget](https://docs.datadoghq.com/dashboards/widgets/slo/)
- [Heatmap widget](https://docs.datadoghq.com/dashboards/widgets/heatmap/)
- [Scatter widget](https://docs.datadoghq.com/dashboards/widgets/scatter_plot/)
