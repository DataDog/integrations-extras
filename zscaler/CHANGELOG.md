# CHANGELOG - ZScaler

## 2.1.0 / 2026-05-04

**Added**

* Added OCSF 1.5.0 normalization for every `zscalernss-*` log type. Each
  log routes through exactly one OCSF sub-pipeline based on sourcetype
  (and, for CASB, severity):

  * `zscalernss-web` → HTTP Activity [4002]
  * `zscalernss-fw` → Network Activity [4001]
  * `zscalernss-dns` → DNS Activity [4003]
  * `zscalernss-tunnel` → Tunnel Activity [4014]
  * `zscalernss-emaildlp` → Data Security Finding [2006]
  * `zscalernss-endpointdlp` → Data Security Finding [2006]
  * `zscalernss-casb` (with severity) → Data Security Finding [2006] (CASB DLP)
  * `zscalernss-casb` (no severity) → File Hosting Activity [6006]
  * `zscalernss-audit` (`LOGIN` / `AUTH`) → Authentication [3002]
  * `zscalernss-audit` (`USER_MANAGEMENT` / `ROLE_MANAGEMENT`) → Account Change [3001]
  * `zscalernss-audit` (any other category) → API Activity [6003]
  * everything else → Base Event [0]

* `OCSF pre transformations` sub-pipeline (runs on all logs):

  * Sets `ocsf.metadata.product.vendor_name` = `"Zscaler"`,
    `ocsf.metadata.product.name` = `"ZIA"`, and
    `ocsf.metadata.product.feature.name` to the sourcetype suffix
    (`web` / `fw` / `dns` / `tunnel` / `casb` / `emaildlp` /
    `endpointdlp` / `audit`).
  * Parses `zscaler.datetime` directly to `ocsf.time` as epoch-ms.
  * Maps `sourcetype` → `ocsf.metadata.log_name`.

* `Build ocsf.file.hashes MD5 entry` and `Build ocsf.file.hashes SHA-256
  entry` sub-pipelines construct the OCSF `file.hashes[]` array from
  `zscaler.filemd5` / `zscaler.filesha` (algorithm + algorithm_id +
  value, appended via `array-processor`). Gated on
  `@sourcetype:(zscalernss-emaildlp OR zscalernss-endpointdlp OR
  zscalernss-casb)` so non-file-bearing logs never receive a
  `file.hashes` array.

* `CASB file name parsing` sub-pipelines (one per object slot) map
  `zscaler.object_name_1` / `zscaler.object_name_2` →
  `ocsf.file.name` when the corresponding
  `zscaler.object_type_name_1` / `_2` is `"File"`.

* Per OCSF sub-pipeline:

  * `schema-category-mapper` for `ocsf.severity_id`:
    * DLP variants: from `zscaler.severity` (`"Info Severity"` / `"Low Severity"` /
      `"Medium Severity"` / `"High Severity"` / `"Critical Severity"` →
      1 / 2 / 3 / 4 / 5).
    * FW Network Activity and HTTP Activity: from
      `zscaler.threatseverity` (lowercased by pre-OCSF grok:
      `informational` / `low` / `medium` / `high` / `critical`),
      falling back to `Informational` / `1`.
    * Audit (Authentication / Account Change / API Activity), DNS,
      Tunnel, File Hosting, Base Event: static `Informational` / `1`
      (NSS doesn't emit a severity for these).
  * `schema-category-mapper` for `activity_id`, `status_id`,
    `tunnel_type_id`, `data_security.detection_system_id` /
    `data_lifecycle_state_id`, `device.type_id`, `file.type_id`, etc.,
    as relevant to each class.
  * `Other` / `99` catch-alls with `fallback:` blocks that copy the
    source field's literal value into the OCSF `*_name` target,
    preserving the vendor's label rather than collapsing to `"Other"`.
    Applied to HTTP Activity `activity_id` (from
    `zscaler.requestmethod`), File Hosting `activity_id` (from
    `zscaler.activity_type_name`), Endpoint DLP `device.type_id` (from
    `zscaler.devicetype`), and Endpoint DLP `file.type_id` (from
    `zscaler.itemtype` / `zscaler.filetypecategory`).
  * Self-mappers for every field set by upstream string-builder /
    attribute-remapper / grok-parser, so the schema-processor recognises
    them.

* Tunnel Activity `ocsf.device.ip` ← `zscaler.sourceip` to satisfy the
  OCSF `at_least_one` constraint on the `device` object
  (`hostname` / `instance_uid` / `interface_name` / `interface_uid` /
  `ip` / `name` / `uid`). `zscaler.sourceip` is the customer-side
  tunnel endpoint per the Zscaler NSS feed format; `destinationip`
  (the Zscaler edge VIP, `%s{destvip}`) is mapped to
  `ocsf.dst_endpoint.ip`.

* OCSF facets: `activity_id` / `activity_name`,
  `category_uid` / `category_name`, `class_uid` / `class_name`,
  `severity_id` / `severity`, `status_id` / `status`,
  `metadata.product.feature.name`, `finding_info.title`,
  `data_security.detection_system` / `detection_pattern`,
  `tunnel_type` / `tunnel_type_id`, `file.name` / `file.type` /
  `file.hashes`, `src_endpoint.ip` / `dst_endpoint.ip`,
  `actor.user.name` / `actor.user.email_addr`, etc.

* 11 OCSF test cases (one per sub-pipeline class) covering every
  routing branch above.

**Changed**

* Pre-OCSF firewall protocol mapper now reads from both
  `zscaler.proto` (the documented NSS feed field) and
  `zscaler.ipproto`.

* Account Change postaction handling: removed
  `zscaler.resource → ocsf.user.name` (`resource` is the role name for
  `ROLE_MANAGEMENT` events, not a user). Replaced with
  `postaction.name` / `postaction.roleName` and `postaction.email`
  mappings for both `USER_MANAGEMENT` and `ROLE_MANAGEMENT` branches.

* Authentication: `zscaler.recordid` now maps to `ocsf.metadata.uid`
  instead of `ocsf.session.uid` (recordid doesn't persist across a
  login session).

* Endpoint DLP `data_security.detection_system_id` corrected from
  `Endpoint` / `1` (EDR) to `Data Loss Prevention` / `2`. EDR is a
  different OCSF detection system; Endpoint DLP is DLP.

* `zscalernss-fw` Network Activity filter admits
  `ipsrulelabel:None` / `threatname:None` placeholder values — the
  documented Zscaler firewall feed populates these placeholders on
  non-threat policy events too.

* Restored `Total Bytes`, `Zscaler Request Size`, and `Zscaler Response
  Size` facets' `type: integer` + `unit: {family: bytes, name: byte}`
  metadata so range filtering and byte-formatted display still work.

* Several existing pre-OCSF `attribute-remapper`s flipped from
  `preserveSource: false` to `preserveSource: true` (e.g. `clt_sip` →
  `network.client.ip`, `srv_dip` → `network.destination.ip`,
  `dns_req` → `dns.question.name`) so the OCSF sub-pipelines can still
  read the original `zscaler.*` fields. No existing attribute paths
  were deleted.

**Removed**

* Previous synthetic `zscalernss-alert` handling: the pre-pipeline that
  fabricated a `sourcetype` from `alertId`, the pre-OCSF `Alert`
  description-grok, and the OCSF "ZIA Alert" sub-pipeline. Real Zscaler
  "alerts" are NSS DLP / CASB logs identified by severity, which now
  route to Data Security Finding [2006]; web / fw traffic stays in
  HTTP Activity [4002] / Network Activity [4001] regardless of
  severity, with no synthetic Detection Finding [2004] sub-pipeline.

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
