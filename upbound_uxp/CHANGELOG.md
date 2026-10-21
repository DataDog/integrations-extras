# CHANGELOG - Upbound UXP

## 1.1.0 / 2026-10-19

***Changed***

* **Behaviour change:** Prometheus counters, and the `_sum` and `_count` samples of histograms and summaries, are now submitted as monotonic counts. Their values in Datadog now represent the increase per collection interval instead of the cumulative total. Dashboards and monitors built on the previous cumulative values (for example using `monotonic_diff`) need to be reviewed. As with any monotonic count, the first collection after an Agent restart produces no value for these metrics.

***Fixed***

* Apply the instance `tags` to all metrics, service checks and the `uxp.datadog_agent_checks` heartbeat. This includes the tags the Cluster Agent adds to dispatched cluster checks (for example `kube_cluster_name`), which were previously dropped.
* Summary quantiles and gauges whose name ends in `_count` are now submitted as gauges instead of counts.

## 1.0.0 / 2023-07-01

***Added***

* Initial Release
