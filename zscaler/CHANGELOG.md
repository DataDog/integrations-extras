# CHANGELOG - ZScaler

## 2.1.0 / 2026-04-21

**Added**

* Added OCSF normalization for all Zscaler NSS log types. Each log type is mapped
  to the appropriate OCSF 1.5.0 class:
  * `zscalernss-web` → HTTP Activity [4002]
  * `zscalernss-dns` → DNS Activity [4003]
  * `zscalernss-fw` (threat-detected) → Detection Finding [2004]
  * `zscalernss-fw` (policy allow/deny) → Network Activity [4001]
  * `zscalernss-tunnel` → Tunnel Activity [4014]
  * `zscalernss-casb` → File Hosting Activity [6006]
  * `zscalernss-emaildlp` → Data Security Finding [2006]
  * `zscalernss-endpointdlp` → Data Security Finding [2006]
  * `zscalernss-audit` (`LOGIN` category) → Authentication [3002]
  * `zscalernss-audit` (`USER_MANAGEMENT` or `ROLE_MANAGEMENT` category) → Account Change [3001]
  * `zscalernss-audit` (any other category) → API Activity [6003]
  * `zscalernss-alert` (ZIA + UEBA) → Detection Finding [2004]
  * All other logs → Base Event [0]
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
