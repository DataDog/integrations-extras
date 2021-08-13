# CHANGELOG - RedisEnterprise


1.0.0
=====

### Fix redirect error on cluster follower

* [Bug] The http wrapper did not honor settings to not follow redirects - confirmed with Datadog team


0.3.1
=====

### Fix for cluster with no databases created

* [Bug] This stops the integration from throwing an error when there are no databases create on the cluster
