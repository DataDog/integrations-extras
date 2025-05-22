# Akamas

## Overview

Akamas helps developers, DevOps, and SREs to easily optimize applications resource inefficiencies, performance and reliability issues in Kubernetes environments. Akamas uniquely provides full-stack recommendations, covering pod sizing, JVM and Node.js heap and GC options, and cluster autoscaling insights.

Thanks to this integration, you can view Akamas identified efficiency and reliability optimization opportunities within the Datadog UI. 

Akamas collects metrics from Datadog related to your Kubernetes environment, including both infrastructure (cluster, nodes, workloads) and applications (e.g. JVM or Node.js). Akamas analyzes the collected metrics, identifies optimization opportunities and sends them to the Datadog platform as events.

## Setup

1.  Log into your Akamas Insights instance.
2.  Navigate to **Datasources** > **Datadog**
3.  Specify the [Datadog site parameter][1] (e.g. US1, EU1..).
4.  Enter your Datadog API key and Application key.
5.  Click "Test Connection" to verify the integration is working.


## Uninstallation

1.  Log into your Akamas Insights instance.
2.  Navigate to **Datasources** > **Datadog**
3.  Click the "Delete" button.

## Support

Need help? Contact [Akamas support][2].


[1]: https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site
[2]: mailto:support@akamas.io