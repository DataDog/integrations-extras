# CHANGELOG - Mergify

## 1.0.1

***Added:***

* Updated the default dashboard with the metrics, added and modified, in 0.1.0 and 1.0.0
* Added a WARNING service check that will be triggered when the user or organization, that the tokens belongs to, is rate limited on GitHub

## 1.0.0

***Changed:***

* Changed default value of `min_collection_interval` to 120

***Added:***

* Refactored the `queue_checks_outcome` metric to have each outcome as a tag, instead of a metric per outcome.
* `mergify_api_url` is now an optional attribute in the config
* Added missing metrics in manifest.json

## 0.1.0

***Added:***

* Added `time_to_merge` metrics
* Added `queue_checks_outcome` metrics
