# CHANGELOG - Cloudsmith

### 1.1.1 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [2829](@https://github.com/DataDog/integrations-extras/pull/2829)

### 1.1.0 / 2025-06-20

***Added***:

* Support for metrics on configured quota limits
* Excluded API token from risk-level emitted events
* Improved logic to prevent duplicate license policy violation events

### 1.0.0 / 2025-06-06

***Added***:

* Metric support for storage usage, bandwidth usage, token usage, and member activity
* Event support for security vulnerability scan results, audit logs, policy violations related to vulnerabilities, and license compliance

### 0.0.2 / 2021-09-08

***Added***:

## 0.0.3 / 2025-10-29

### Added

* Metric: `cloudsmith.bandwidth_bytes_interval` for real-time bandwidth tracking, through Cloudsmith v2 analytics endpoint (disabled by default; enable with `enable_realtime_bandwidth: true`). Uses fixed internal defaults (1-minute interval, aggregate `BYTES_DOWNLOADED_SUM`, look-back 120m, refresh 300s, min points 2).
* Dashboard widget for realtime interval bytes.
