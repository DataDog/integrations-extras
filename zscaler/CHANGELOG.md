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
