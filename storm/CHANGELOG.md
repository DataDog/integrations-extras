# CHANGELOG - Storm

1.1.1/ Released
=================

### Changes

* [UPDATE] Make backwards compatible with storm [1.0.0, 1.2.0).
* [FIX] Make this more robust to api errors.

1.0.2/ Released
=================

### Changes

* [FIX] Cluster metrics sent with 0 values if unable to connect to Storm UI. Now bails on ConnectionErrors.
* [FIX] If on Agent6 - TypeError: gauge() got an unexpected keyword argument 'metric'
* [UPDATE] Redundant environment tags. stormEnvironment replaces env/environment/stormClusterEnviroment to reduce number of metrics.

1.0.1/ Released
=================

### Changes

* [UPDATE] Updated storm bin to 1.2, and forked storm binary blob to prevent future CI breakage

1.0.0/ Released
=================

### Changes

* [FEATURE] adds storm integration.
