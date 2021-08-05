# Redis Enterprise

![img](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/redis-enterprise.jpg)

## Overview

This integration provides [Redis Enterprise][1] monitoring and metrics for Datadog.

### What is Redis Enterprise?

[Redis Enterprise][1] is the fully supported enterprise version of Redis.  In addition to the core open source Redis feature set, Redis Enterprise adds active-active geo-distribution, multi-model database features, enhanced observability and easier multi-tenancy management for higher uptimes.

### Redis Enterprise Datadog Dashboard

Redis Enterprise's Datadog integration provides a templated view across your clusters and databases allowing for operational insight unavailable in other products. Understand usage patterns and plan for growth armed with the data necessary to make informed decisions.

#### Database Overview
![overview](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/dashboard.png)

#### Cluster Overview
![overview](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/datadog_cluster_top_view.png)

#### Redis on Flash
![rofdash](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/ROF_dashboard.png)

#### Redis Enterprise Events
![events](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/events.png)


### Provider

![dashboard](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/redislabs-logo.png)

This integration is provided by Redis Labs.



## Setup

Copy the [sample configuration][2] and update the required sections to collect data from your Redis Enterprise cluster

```yml
    ## @param host - string - required
    ## The RedisEnterprise host
    #
    host: myrediscluster.example.com

    ## @param port - integer - optional - default: 9443
    #
    port: 9443

    ## @param user - string - required
    ## The RedisEnterprise API user
    #
    username: redisadmin@example.com

    ## @param password - string - required
    ## The RedisEnterprise API credential
    #
    password: mySecretPassword
```

See the full example file for other optional settings available to match your cluster configuration.

Users can be configured according to the [documentation][3].

## Data Collected

### Metrics

See [metadata.csv][4] for a list of metrics provided by this integration and the description of each.

### Service Checks

**`redisenterprise.running`**

The check returns:

- `OK` if the RedisEnterprise cluster API is properly responding to commands
- `CRITICAL` if the API is not properly responding

**`redisenterprise.license_check`**

The check returns:

- `OK` if the cluster license is valid for longer than 1 week.
- `WARNING` if cluster license will expire in < 7 days.
- `CRITICAL` if the cluster license has expired.

**Note:** The cluster will continue to operate as normal with an expired license, however, no configuration changes can be made during this time.  Contact your sales representative for a renewal.


### Events

All [Redis Enterprise events][5] are collected.

## Troubleshooting

Contact the [Redis Enterprise Support Team][6]


[1]: http://www.redislabs.com
[2]: https://github.com/DataDog/integrations-extras/blob/master/redisenterprise/datadog_checks/redisenterprise/data/conf.yaml.example
[3]: https://docs.redislabs.com/latest/rc/security/database-security/passwords-users-roles/
[4]: https://github.com/DataDog/integrations-extras/blob/master/redisenterprise/metadata.csv
[5]: https://docs.redislabs.com/latest/rs/administering/monitoring-metrics/#cluster-alerts
[6]: https://redislabs.com/deployment/support/
