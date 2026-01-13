# CHANGELOG - Auth0

## 2026-01-13

### Added
- Introduced a new metric:
  - `auth0.api_request.count` (type: count)
    - Description: Requests received by a given tenant/s in Auth0.
    - Tags / sample tags: `api`, `operation_name`, `operation_result`, `tenant`, `failure_code`, `client_id`, `connection_id`, `grant_type`
    - Example metric queries used in the included dashboard:
      - `sum:auth0.api_request.count{...}.as_count()`
      - `sum:auth0.api_request.count{...}.as_rate().rollup(sum, 1)`

- Dashboards:
  - Added `auth0/assets/dashboards/auth0-api-usage.json`
    - Title: "My Auth0 API Usage Dashboard"
    - Provides widgets for:
      - Request trends by operation/result
      - Failure breakdowns (global and operation rate limits)
      - Requests per path and operation
      - Quota/throughput metrics (RPS, p50/p90/p99, max/avg)
    - Includes template variables: `tenant`, `api`, `client_id`, `grant_type`
- Images
  - Added a screenshot of the new Auth0 API Usage dashboard `auth0/images/apiUsageDashboard.png`

### Notes
- No breaking changes.
- No special migration steps required. The new metric will appear once the integration sends metric data (ensure Auth0 log streaming and any metric forwarding are configured as needed).
- Suggested first steps after deploying:
  1. Navigate to Datadog -> Metrics -> Explorer and search for `auth0.api_request.count`.
  2. Import or open the provided dashboard at `auth0/assets/dashboards/auth0-api-usage.json` to get an out-of-the-box view of API usage and failures.

### Files changed (in this branch)
- `auth0/README.md` - README updated to reference metrics
- `auth0/metadata.csv` - new metric entry added
- `auth0/assets/dashboards/auth0-api-usage.json` - new dashboard added
