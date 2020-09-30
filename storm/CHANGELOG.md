# CHANGELOG - Storm

## 1.0.1 / 2020-09-29

* [Fixed] Fix response parsing. See [#724](https://github.com/DataDog/integrations-extras/pull/724).


## 1.0.0 / 2020-07-27

* [UPDATE] Make backwards compatible with storm [1.0.0, 1.2.0).
* [FIX] Make this more robust to api errors.
* [FIX] Cluster metrics sent with 0 values if unable to connect to Storm UI. Now bails on ConnectionErrors.
* [FIX] If on Agent6 - TypeError: gauge() got an unexpected keyword argument 'metric'
* [UPDATE] Redundant environment tags. stormEnvironment replaces env/environment/stormClusterEnviroment to reduce number of metrics.
* [UPDATE] Updated storm bin to 1.2, and forked storm binary blob to prevent future CI breakage
* [FEATURE] adds storm integration.
