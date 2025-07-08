# Gatling Enterprise

## Overview

Gatling Enterprise is a load testing platform designed to help teams validate application scalability and performance under real-world traffic conditions.

With the Datadog integration, teams can investigate performance issues by correlating load test metrics such as response times, throughput, and errors with infrastructure data tracked in Datadog.

Gatling Enterprise sends metrics to Datadog, allowing engineering and SRE teams to centralize performance insights and improve decision-making around scalability and reliability.


## Setup

> **Note**: This integration is available for Gatling Enterprise customers. To learn more about Gatling Enterprise and get started for free, visit [gatling.io/products][1].

1. In Datadog, navigate to **Integrations**, select the Gatling Enterprise tile, and click **Install Integration**.

2. In your Gatling control-plane installation, edit your [configuration file][2]. In the section `system-properties`, add the parameters as follows. Replace YOUR_API_KEY with your [Datadog API key][3] and use the correct [Datadog site][4] for your organization:

```bash
control-plane {
  locations = [
    {
      id = "prl_example"
      # ... other configuration for your location
      system-properties {
        "gatling.enterprise.dd.api.key" = "YOUR_API_KEY" # Fill your API key here
        "gatling.enterprise.dd.site" = "datadoghq.com"  # Replace with your Datadog site
      }
    }
  ]
}
```

3. Deploy and restart your control plane


## Data Collected

The Gatling Enterprise integration gathers all metrics for databases, nodes, and shards.


### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

## Uninstallation

1. In Datadog, navigate to **Integrations**, select the Gatling Enterprise tile, and click **Uninstall Integration**.

2. In your Gatling control-plane installation, edit your [configuration file][5]. In the section `system-properties`, remove the lines containing `gatling.enterprise.dd`.
   
3. Deploy and restart your control plane.

## Support

Need help? Contact [Gatling Enterprise support][7].



[1]: https://gatling.io/products
[2]: https://docs.gatling.io/reference/install/cloud/private-locations/introduction/
[3]: https://docs.datadoghq.com/account_management/api-app-keys/
[4]: https://docs.datadoghq.com/getting_started/site/
[5]: https://docs.gatling.io/reference/install/cloud/private-locations/introduction
[6]: https://github.com/DataDog/integrations-extras/blob/master/gatling_enterprise/metadata.csv
[7]: https://gatlingcorp.atlassian.net/servicedesk/customer/portal/8
