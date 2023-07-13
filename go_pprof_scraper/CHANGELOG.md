# CHANGELOG - Go-pprof-scraper

## 1.0.4 / 2023-01-17

***Added***: 

* Add documentation on configuring TLS for profile collection.

## 1.0.3 / 2023-01-17

***Fixed***: 

* The `pprof_url` parameter no longer requires a trailing "/" to work properly.

## 1.0.2 / 2022-12-27

***Fixed***: 

* Decrease `min_collection_interval` value to prevent long pause between collecting profiles.
* Properly encode the socket path in the trace agent's profiling endpoint URL when sending profiles over UDS.

## 1.0.1 / 2022-11-10

***Added***: 

* Add Go pprof scraper integration. See [#1541](https://github.com/DataDog/integrations-extras/pull/1541).
