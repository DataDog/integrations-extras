# CHANGELOG - ZScaler

## 2.1.0 / 2026-04-21

**Added**

* Added OCSF normalization for all Zscaler NSS log types. Each log type is mapped
  to the appropriate OCSF 1.5.0 class:
  * **`zscalernss-web` or `zscalernss-fw` with `zscaler.threatseverity`
    set and not `None`/`none`** → Detection Finding [2004] (Alert) —
    takes precedence over the per-log-type web/fw classes below
  * `zscalernss-web` (no threatseverity) → HTTP Activity [4002]
  * `zscalernss-dns` → DNS Activity [4003]
  * `zscalernss-fw` (threat-detected, no threatseverity) → Detection Finding [2004]
  * `zscalernss-fw` (policy, no threatseverity) → Network Activity [4001]
  * `zscalernss-tunnel` → Tunnel Activity [4014]
  * `zscalernss-casb` (with severity) → Data Security Finding [2006] (CASB DLP)
  * `zscalernss-casb` (no severity) → File Hosting Activity [6006]
  * `zscalernss-emaildlp` → Data Security Finding [2006]
  * `zscalernss-endpointdlp` → Data Security Finding [2006]
  * `zscalernss-audit` (`LOGIN` category) → Authentication [3002]
  * `zscalernss-audit` (`USER_MANAGEMENT` or `ROLE_MANAGEMENT` category) → Account Change [3001]
  * `zscalernss-audit` (any other category) → API Activity [6003]
  * All other logs → Base Event [0]
* Removed the previous synthetic `zscalernss-alert` handling: the
  pre-pipeline that fabricated a `sourcetype` from `alertId`, the
  pre-OCSF `Alert` description-grok, and the OCSF "ZIA Alert"
  sub-pipeline. Real Zscaler "alerts" are NSS web/fw/DLP/CASB logs
  with an alert-worthy severity, not a separate webhook payload, so
  the new severity-based Alert sub-pipeline replaces all of it.
* Set `ocsf.metadata.product.name` to `"ZIA"` (the product) and
  `ocsf.metadata.product.feature.name` to the sourcetype suffix
  (`fw`, `dns`, `web`, `tunnel`, `casb`, `emaildlp`, `endpointdlp`, `audit`,
  `alert`). `ocsf.metadata.product.vendor_name` is `"Zscaler"`.
* Added OCSF facets (activity, category, class, status, severity,
  finding_info, file, tunnel_type, data_security, api.operation,
  product.feature.name, etc.).
* Added OCSF test expectations for all 12 test cases (one new test case
  added to exercise Network Activity for a non-threat fw Allow event).
* Aligned OCSF schema-category-mapper filters with the values actually
  emitted by NSS:
  * Firewall threat severity filters use lowercase
    (`informational`/`low`/`medium`/`high`/`critical`) to match the
    pre-OCSF lowercase normalization of `zscaler.threatseverity`.
  * Email DLP and Endpoint DLP severity filters use the literal NSS
    labels (`"Info Severity"`, `"Low Severity"`, `"Medium Severity"`,
    `"High Severity"`, `"Critical Severity"`).
  * Firewall protocol mapper reads from both `zscaler.proto` (the
    field name in the documented NSS feed format) and
    `zscaler.ipproto`.
  * Wildcard catch-alls in OCSF schema-category-mappers now emit
    `Other`/`99` (rather than `Unknown`/`0`) when a known source
    field carries a value that doesn't map to an OCSF enum entry.
    This preserves the vendor's signal in the OCSF output rather
    than collapsing all unmapped values to `Unknown`. The single
    numeric-range catch-all (`zscaler.threat_score`) still uses
    `Unknown`/`0` since there's no categorical label to preserve.
  * Replaced hardcoded `string-builder-processor` pairs (one for the
    OCSF enum name, one for its id) with single
    `schema-category-mapper` blocks across FW Detection Finding,
    ZIA Alert, Email DLP, Endpoint DLP, and Authentication
    sub-pipelines. More compact and better leverages the
    schema-processor.
  * Replaced two-step "build string then grok-parse to array"
    patterns with `array-processor` for `ocsf.finding_info.data_sources`
    and `ocsf.finding_info.types` in alert sub-pipelines.
  * `Map zscaler.time directly to date` via grok-parser, removing
    the intermediate `zscaler.time → zscaler.datetime` attribute-
    remapper (audit logs use `time`, not `datetime`).
  * Activity count grok now writes directly to
    `ocsf.finding_info.related_events_count` instead of an
    intermediate `activity_count` field.
  * Removed the `Map alertId to ocsf.metadata.event_code` mapping
    (alertId is the alert's uid, not its event_code) and added a
    direct `ruleName → ocsf.metadata.event_code` mapping. Rule name
    is the canonical event_code per OCSF guidance.
  * Removed the `Map zscaler.resource to ocsf.user.name` mapping in
    the Account Change sub-pipeline (`resource` is the role name
    for `ROLE_MANAGEMENT` events, not a user). Replaced with
    `postaction.name`/`postaction.roleName` and
    `postaction.email` mappings for both USER_MANAGEMENT and
    ROLE_MANAGEMENT branches.
  * Account Change and Authentication severity is now
    always-`Informational/1` rather than derived from
    `zscaler.result` SUCCESS/FAILURE — audit events are operational,
    not security findings, and NSS doesn't emit a severity field
    for them.
  * Authentication `zscaler.recordid` now maps to
    `ocsf.metadata.uid` instead of `ocsf.session.uid` (recordid
    doesn't persist across a login session).
  * Removed redundant `string-builder-processor` for
    `ocsf.metadata.product.feature.name` in the alert sub-pipeline
    (the pre-transformation grok already populates it from the
    sourcetype suffix).
  * Endpoint DLP `data_lifecycle_state` now matches the
    `activitytype` values actually emitted by NSS (`email_sent`,
    `EMAIL_SENT`, `FILE_UPLOAD`, `PRINT`), with `Other/99`
    catch-all.
  * Endpoint DLP `data_security.detection_system_id` corrected
    from `Endpoint`/`1` (EDR) to `Data Loss Prevention`/`2`. EDR
    is a different OCSF detection system; Endpoint DLP is DLP.
  * Single-category schema-category-mappers now include an
    explicit `Other`/`99` catch-all alongside their primary
    category. This is defensive — the catch-all should never fire
    given the sub-pipeline's own filter — but it makes the mapping
    explicit and graceful if the sub-pipeline filter ever changes.
    Applied to FW Detection Finding `activity_id`, Email DLP
    `activity_id` / `detection_system_id` /
    `data_lifecycle_state_id`, Endpoint DLP `activity_id` /
    `detection_system_id`, FW Detection Finding and ZIA Alert
    `finding_info.analytic.type_id`.

## 2.0.0 / 2025-08-27

**Changed**:

* Updated pipeline for web, firewall, DNS, and Tunnel logs.
* Update overview dashboard.

**Added**

* Added support for SaaS security, SaaS security activity, admin audit, endpoint DLP, email DLP and alert logs.
* Added dashboards and detection rules.

## 1.0.0

**Added**

* Initial Release
