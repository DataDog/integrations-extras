# CHANGELOG - Cloudsmith

### 1.3.0 / 2026-03-03

### Added

* Org-wide realtime bandwidth monitoring (`enable_realtime_bandwidth`, default `true`) — submits `cloudsmith.bandwidth.bytes_downloaded` and `cloudsmith.bandwidth.request_count` for the entire organization with no filters
* Allow different profiles (with custom filters) to extract more granular bandwidth data
* New dashboard group "Org Bandwidth Overview" with query-value and timeseries widgets
* Added repository-level gauges from `/repos/{owner}/` for live repository storage and operational counters: `cloudsmith.repository.storage_bytes`, `cloudsmith.repository.package_count`, and `cloudsmith.repository.download_count`
* New dashboard group "Repository Overview" with repository-filtered query values and top lists for storage, package count, and download count

### FIXED

* Quota endpoint converations were off by slight margin, this has now been resolved

### 1.2.0 / 2025-11-03

### Added

* Added real-time bandwidth metric (`cloudsmith.bandwidth_bytes_interval`) and related dashboard widget

### 1.1.1 / 2025-10-17

***Added***

* Upgrade the datadog-checks-base to `37.20.0` [#2829](https://github.com/DataDog/integrations-extras/pull/2829)

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
