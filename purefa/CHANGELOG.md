# CHANGELOG - PureFA

## 1.1.1 / 2023-04-28
* [Fixed] Remove the use_latest_spec option from the config file. See [#1835](https://github.com/DataDog/integrations-extras/pull/1835).

## 1.1.0

* [Added] Support for [Pure FlashArray OpenMetrics Exporter](https://github.com/PureStorage-OpenConnect/pure-fa-openmetrics-exporter)
* [Deprecated] Support for the [Pure Exporter](https://github.com/PureStorage-OpenConnect/pure-exporter) - Deprecated metrics names are listed in `metadata.csv` as `Legacy`

## 1.0.1

* [Fixed] Updated purefa.py to include a default `openmetrics_endpoint` from `spec.yaml`

## 1.0.0

* [Added] Initial Pure Storage FlashArray integration.
