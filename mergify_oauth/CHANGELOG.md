# CHANGELOG - Mergify

## 2.0.0 / 2026-06-18

***Removed***:

* The **Mergify Merge Queue Overview** dashboard, superseded by the new Stats dashboard.
* `mergify.queue_freeze.duration`, a metric that never reported data.

***Changed***:

* Refreshed the integration overview and documented every queue `outcome` and `exit_reason` value.

***Deprecated***:

* The legacy operational metrics `mergify.merge_queue_length`, `mergify.time_to_merge.*`, and `mergify.queue_checks_outcome` are superseded by the new `mergify.queue.*` metrics (`mergify.queue.size.max`, `mergify.queue.total_queue_time`, and `mergify.queue.check_outcome` respectively).

***Added***:

* Merge queue Stats parity: 19 new `mergify.queue.*` metrics covering throughput (pull requests entered and merged, queue and batch size), queue health (exit reasons, check outcomes, CI retries, and bisections), and performance (queue time, CI runtime, and idle waits) — all tagged by repository, branch, queue, and priority rule.
* An out-of-the-box **Mergify - Merge Queue Stats** dashboard that mirrors your Mergify Stats page.

## 1.0.0 / 2024-10-02

***Added***:

* Initial Release
