# CHANGELOG - Cloudsmith

## [1.0.0] - 2025-05-01

### Added
- Initial production release of the Cloudsmith Datadog integration.
- Metrics for:
  - Storage usage:
    - `cloudsmith.storage_used`: Storage usage percentage.
    - `cloudsmith.storage_used_bytes`: Raw storage used in bytes.
    - `cloudsmith.storage_peak_bytes`: Peak storage usage in bytes.
    - `cloudsmith.storage_configured_bytes`: Configured storage capacity in bytes.
  - Bandwidth usage:
    - `cloudsmith.bandwidth_used`: Bandwidth usage percentage.
    - `cloudsmith.bandwidth_used_bytes`: Raw bandwidth used in bytes.
    - `cloudsmith.bandwidth_configured_bytes`: Configured bandwidth capacity in bytes.
  - Token usage:
    - `cloudsmith.token_count`: Number of entitlement tokens in the org.
    - `cloudsmith.token_bandwidth_total`: Total bandwidth used by tokens.
    - `cloudsmith.token_download_total`: Total downloads served via tokens.
  - Member metrics:
    - `cloudsmith.member.active`: Total active members.
    - `cloudsmith.member.role.owner`, `.manager`, `.member`: Member counts by role.
    - `cloudsmith.member.has_2fa`: Members with 2FA enabled.
- Events:
  - Security vulnerability scan results (`@aggregation_key:vulnerabilities`)
  - Audit log activity (`@aggregation_key:audit_log`)
  - Policy violations for vulnerabilities and license compliance
- Support for `cloudsmith.members` data collection and Datadog event enrichment including detailed summaries and table-style logs.