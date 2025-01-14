# CHANGELOG - neo4j

## 3.0.4 / 2024-04-06

***Changed***:

* Updated the conf.yaml.example to clarify how to monitor multiple databases and set the example database version to 5.18.
* Updated the conf.yaml.example to remove references to Neo4j 3.5

***Added***:

* Added additional bolt, page_cache eviction and relationship type  metrics which have been introduced since Neo4j 5.10

## 3.0.3 / 2024-04-05

***Fixed***:

* Fixes db_name tagging regression introduced by 00830c1 - PR [2314](https://github.com/DataDog/integrations-extras/pull/2314)

## 3.0.2 / 2023-10-31

***Changed***:

* Config models update - PR [2088](https://github.com/DataDog/integrations-extras/pull/2088)

## 3.0.1 / 2023-07-05

***Added***:

* Added server routing metrics which were introduced in Neo4j 5.10

## 3.0.0 / 2023-06-02

***Added***:

* Update Neo4j Integration to support Neo4j 5. 
* Added addtional [metrics](https://neo4j.com/docs/operations-manual/5/monitoring/metrics/reference/) to support Neo4j 5.

## 2.0.2 / 2023-04-28

***Changed***:

* Remove the use_latest_spec option from the config file.

## 2.0.1 / 2022-08-22

***Added***:

* Added causal_cluster read replica metrics ([#1509](https://github.com/DataDog/integrations-extras/pull/1509))

## 2.0.0 / 2022-02-24

***Changed***:

* Update Neo4j Integration to Support Neo4j 4.x ([#944](https://github.com/DataDog/integrations-extras/pull/944). Thanks [davidfauth](https://github.com/davidfauth))

***Added***:

* Add curated_metric column to metadata.csv files ([#1209](https://github.com/DataDog/integrations-extras/pull/1209))
* Validate config files ([#1001](https://github.com/DataDog/integrations-extras/pull/1001))

## 1.0.1 / 2021-07-28

***Added***:

* Update neo4j check to use requests wrapper ([#894](https://github.com/DataDog/integrations-extras/pull/894))
