# OceanBase Cloud Integration

## Overview

[OceanBase Database][1] is a distributed relational database. OceanBase Database adopts an independently developed integrated architecture, which encompasses both the scalability of a distributed architecture and the performance advantage of a centralized architecture. 

[OceanBase Cloud][2] provides fully managed database services with elastic scalability, ultra-fast performance, and high compatibility on global cloud infrastructure.

With the Oceanbase Cloud integration, users can collect various monitoring data for database clusters created on OceanBase Cloud in Datadog, including operating status, cluster performance, and cluster health.

## Setup

To set up the OceanBase Cloud Datadog integration for your cluster, please refer to the following steps
1. Log in to the Datadog console.    
    a. Choose the right site from [Datadog sites][3].    
    b. Log in using your Dotadog credentials.
2. Log in to the OceanBase Cloud console using your OceanBase Cloud credentials, navigate to the [Integrations][4] page, and search for the Datadog integration.
3. Click Connect. You will be redirected to the Datadog authorization page. If you have not logged in to Datadog before this step, you will need to select the appropriate site and log in on the opened authorization page. 
4. Click Authorize. You will then be redirected back to the OceanBase Cloud console. A notification will appear if the authorization is successful. Contact OceanBase Cloud technical support if an error occurs.
5. Search for OceanBase in the Datadog console, and click Install. The monitoring data for your OceanBase Cloud instance will appear in a few minutes on the Datadog Dashboards page.

## Uninstallation

1. Log in to the OceanBase Cloud console, go to [OceanBase Cloud Integrations][4], and search the Datadog product.
2. Click remove button, a notification will be displayed if successful.

Once this integration has been uninstalled, any previous authorizations are revoked.
Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page. 

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.

### Service Checks

The OceanBase Cloud integration does not include any service checks.

### Events

The OceanBase Cloud integration does not include any events.

## Troubleshooting

Need help? Contact [OceanBase support][6].

[1]: https://en.oceanbase.com
[2]: https://en.oceanbase.com/product/cloud
[3]: https://docs.datadoghq.com/getting_started/site
[4]: https://cloud.oceanbase.com/integrations
[5]: https://github.com/DataDog/integrations-extras/blob/master/oceanbasecloud/metadata.csv
[6]: https://en.oceanbase.com/docs/oceanbase-cloud
