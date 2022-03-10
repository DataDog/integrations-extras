# CHANGELOG - RedisEnterprise

1.1.1
=====

### Bug fix for monitors

* [Bug] Unable to get monitor results without a hostname set - fixed

1.1.0
=====

### Add in new Active Active metrics

* [Feature] Collect statistics on Active/Active(CRDT) databases
* [Bug] the http wrapper now allows get params, so revert usage of python requests


1.0.0
=====

### Fix redirect error on cluster follower

* [Bug] The http wrapper did not honor settings to not follow redirects - confirmed with Datadog team


0.3.1
=====

### Fix for cluster with no databases created

* [Bug] This stops the integration from throwing an error when there are no databases create on the cluster
