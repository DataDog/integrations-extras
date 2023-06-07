# CHANGELOG - Mergify

## 1.0.0

* Refactored the `queue_checks_outcome` metric to have each outcome as a tag, instead of a metric per outcome.
* `mergify_api_url` is now an optional attribute in the config
* Added missing metrics in manifest.json
* Changed default value of `min_collection_interval` to 120

## 0.1.0

* Added `time_to_merge` metrics
* Added `queue_checks_outcome` metrics
