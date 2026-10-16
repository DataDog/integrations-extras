# CHANGELOG - Upbound UXP

### Unreleased

### Fixed

* Apply the instance `tags` to all metrics and service checks. This includes the tags the Cluster Agent adds to dispatched cluster checks (for example `kube_cluster_name`), which were previously dropped.
* Submit Prometheus counters, and the `_sum` and `_count` samples of histograms and summaries, as monotonic counts instead of counts of the cumulative value. Summary quantiles and gauges whose name ends in `_count` are now submitted as gauges.

## 1.0.0 / 2023-07-01

***Added***

* Initial Release
