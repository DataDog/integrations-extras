# CHANGELOG - Cloudsmith

### 1.2.0 / 2025-11-03

### Added

* Added real-time bandwidth metric (`cloudsmith.bandwidth_bytes_interval`) and related dashboard widget

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
