# Akamas

## Overview

Akamas helps developers, DevOps, and SREs optimize application performance, reliability, and resource efficiency in Kubernetes environments. Akamas provides full-stack recommendations, from pod sizing and cluster autoscaling to JVM and Node.js heap and garbage collection settings.

With this integration, you can view Akamas-identified efficiency and reliability optimization opportunities directly within Datadog.

Akamas collects Kubernetes-related metrics from Datadog, covering both infrastructure (clusters, nodes, workloads) and applications (e.g., JVM and Node.js). It analyzes these metrics to identify optimization opportunities, which are then sent back to Datadog as events.

## Setup

1.  Log into your Akamas Insights instance.
2.  Navigate to **Datasources** > **Datadog**.
3.  Specify the [Datadog site parameter][1] (for example, US1 or EU1).
4.  Enter your Datadog API key and Application key.
5.  Click **Test Connection** to verify the integration is working.


## Uninstallation

1.  Log into your Akamas Insights instance.
2.  Navigate to **Datasources** > **Datadog**.
3.  Click the **Delete** button.

## Support

Need help? Contact [Akamas support][2].


[1]: https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site
[2]: mailto:support@akamas.io