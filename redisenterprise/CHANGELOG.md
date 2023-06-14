# CHANGELOG - RedisEnterprise

## 1.2.0 / 2023-06-14

* [Added] Use Hatch to manage environments. See [#1669](https://github.com/DataDog/integrations-extras/pull/1669).
* [Added] Update example config files with new metric_patterns option. See [#1250](https://github.com/DataDog/integrations-extras/pull/1250).
* [Added] Add `pyproject.toml` file. See [#1184](https://github.com/DataDog/integrations-extras/pull/1184).
* [Added] Add curated_metric column to metadata.csv files. See [#1209](https://github.com/DataDog/integrations-extras/pull/1209).
* [Fixed] Remove overwriting host references in metric submission. See [#1886](https://github.com/DataDog/integrations-extras/pull/1886).
* [Fixed] Sync config. See [#1689](https://github.com/DataDog/integrations-extras/pull/1689).
* [Fixed] Update conf.yaml.example files. See [#1147](https://github.com/DataDog/integrations-extras/pull/1147).

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
