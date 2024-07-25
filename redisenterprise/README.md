# Redis Enterprise (Deprecated)

![img](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/redis-enterprise.jpg)

## Overview

**This integration is will be deprecated starting on November 1, 2024. Please use the latest [Redis Enterprise Datadog Integration][13] going forward. This new integration exposes all of the latest Redis Enterprise metrics and includes updated dashboards.**

This integration provides [Redis Enterprise][1] monitoring and metrics for Datadog.

### What is Redis Enterprise?

[Redis Enterprise][1] is the fully supported enterprise version of Redis. In addition to the core open source Redis feature set, Redis Enterprise adds active-active geo-distribution, multi-model database features, enhanced observability, and easier multi-tenancy management for higher uptimes.

### Redis Enterprise Datadog dashboard

Redis Enterprise's Datadog integration provides a templated view across your clusters and databases allowing for operational insight unavailable in other products. Understand usage patterns and plan for growth armed with the data necessary to make informed decisions.

#### Database overview
![overview](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/dashboard.png)

#### Cluster overview
![overview](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/datadog_cluster_top_view.png)

#### Redis on Flash
![rofdash](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/ROF_dashboard.png)

#### Active/Active Redis
![rofdash](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/active_active_dashboard.png)

#### Redis Enterprise events
![events](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/events.png)

### Provider

![provider](https://raw.githubusercontent.com/DataDog/integrations-extras/master/redisenterprise/images/logo-redis.png)

This integration is provided by Redis Labs.

## Setup

### Installation

If you are using Agent v7.21+ / v6.21+ follow the instructions below to install the RedisEnterprise check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior < v7.21 / v6.21][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][2].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-redisenterprise==<INTEGRATION_VERSION>
   ```
  You can find the latest version on the [Datadog Integrations Release Page][12]

   **Note**: If necessary, prepend `sudo -u dd-agent` to the install command.
   
3. Configure your integration like [any other packaged integration][6].

### Configuration

Copy the [sample configuration][7] and update the required sections to collect data from your Redis Enterprise cluster

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

Users can be configured according to the [documentation][8].

## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this integration.

### Service Checks

**`redisenterprise.running`**

The check returns:

- `OK` if the RedisEnterprise cluster API is properly responding to commands
- `CRITICAL` if the API is not properly responding

**`redisenterprise.license_check`**

The check returns:

- `OK` if the cluster license is valid for longer than 1 week.
- `WARNING` if cluster license expires in < 7 days.
- `CRITICAL` if the cluster license has expired.

**Note:** The cluster continues to operate as normal with an expired license, however, no configuration changes can be made during this time. Contact your sales representative for a renewal.

### Events

All [Redis Enterprise events][10] are collected.

## Troubleshooting

Contact the [Redis Field Engineering Team][11].


[1]: http://www.redislabs.com
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=agentv721v621
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=agentearlierversions
[5]: https://docs.datadoghq.com/agent/guide/use-community-integrations/?tab=docker
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/redisenterprise/datadog_checks/redisenterprise/data/conf.yaml.example
[8]: https://docs.redislabs.com/latest/rc/security/database-security/passwords-users-roles/
[9]: https://github.com/DataDog/integrations-extras/blob/master/redisenterprise/metadata.csv
[10]: https://docs.redislabs.com/latest/rs/administering/monitoring-metrics/#cluster-alerts
[11]: mailto:redis.observability@redis.com?subject=Datadog%20Integration%20Support
[12]: https://github.com/DataDog/integrations-extras/tags
[13]: https://docs.datadoghq.com/integrations/redis_enterprise/
