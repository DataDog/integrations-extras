# CHANGELOG - Storm

## 1.0.1 / 2020-09-29

***Fixed***: 

* Fix response parsing. See [#724](https://github.com/DataDog/integrations-extras/pull/724).

## 1.0.0 / 2020-07-27

***Added***: 

* Make backwards compatible with storm [1.0.0, 1.2.0).
* Redundant environment tags. stormEnvironment replaces env/environment/stormClusterEnviroment to reduce number of metrics.
* Updated storm bin to 1.2, and forked storm binary blob to prevent future CI breakage
* adds storm integration.

***Fixed***: 

* Make this more robust to api errors.
* Cluster metrics sent with 0 values if unable to connect to Storm UI. Now bails on ConnectionErrors.
* If on Agent6 - TypeError: gauge() got an unexpected keyword argument 'metric'
