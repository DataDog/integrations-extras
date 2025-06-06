# CHANGELOG - Cloudsmith

### 1.1.0 / 2025-06-10

***Added***:
* Metrics for configured quota limits:
  - `cloudsmith.storage_configured_bytes`, `cloudsmith.storage_configured_gb`
  - `cloudsmith.bandwidth_configured_bytes`, `cloudsmith.bandwidth_configured_gb`
* All events now tagged with `source:cloudsmith` and include `source_type_name`.
* Dashboard color updated to reflect Cloudsmith brand blue.

***Fixed***:
* API token no longer exposed in emitted events.
* Logic improved to prevent duplicate license policy violation events.

### 1.0.0 / 2025-06-06

***Added***:

* Metric support for storage usage, bandwidth usage, token usage, and member activity
* Event support for security vulnerability scan results, audit logs, policy violations related to vulnerabilities, and license compliance

### 0.0.2 / 2021-09-08

***Added***:

* Initial Release
