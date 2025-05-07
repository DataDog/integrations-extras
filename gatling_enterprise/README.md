# Gatling Enterprise

## Overview

Gatling Enterprise is a load testing platform designed to help teams validate application scalability and performance under real-world traffic conditions.

With the Datadog integration, teams can investigate performance issues by correlating load test metrics (e.g., response times, throughput, errors) with infrastructure data tracked in Datadog.

Gatling Enterprise sends metrics to Datadog, allowing engineering and SRE teams to centralize performance insights and improve decision-making around scalability and reliability.


## Setup

> **Note:** This integration is available for Gatling Enterprise customers. To learn more about Gatling Enterprise and get started for free, visit[ gatling.io/products][1].

1. In Datadog, navigate to **Integrations**, select the Gatling Enterprise tile, and click **Install Integration.**

2. In your Gatling control-plane installation, edit your [configuration file][2]. In the section `system-properties`, add the parameters as follows:

```bash

control-plane {

  locations = [

    {

      id = "prl_example"

      # ... other configuration for your location

      system-properties {

        "gatling.enterprise.dd.api.key" = "<your api key>" # fill your API key here

        "gatling.enterprise.dd.site" = "datadoghq.com"  # replace with your Datadog site

      }

    }

  ]

}

```

## Uninstallation

1. In Datadog, navigate to **Integrations**, select the Gatling Enterprise tile, and click **Uninstall Integration**.

2. In your Gatling control-plane installation, edit your [configuration file][2]. In the section `system-properties`, remove the lines containing `gatling.enterprise.dd`.

## Support

Need help? Contact [Gatling Enterprise support][4].



[1]: https://gatling.io/products
[2]: <https://docs.gatling.io/reference/install/cloud/private-locations/introduction/>
[4]: https://gatlingcorp.atlassian.net/servicedesk/customer/portal/8