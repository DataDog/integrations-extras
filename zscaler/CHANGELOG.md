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
  * `zscalernss-audit` (SIGN_IN / SIGN_OUT) → Authentication [3002]
  * `zscalernss-audit` (config CRUD) → API Activity [6003]
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
