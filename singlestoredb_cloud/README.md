## Overview

SingleStoreDB Cloud is a distributed, relational database with optimized speed and scalability to support data-intensive and real-time applications. With this integration, you can monitor your SingleStoreDB Cloud databases. To integrate Datadog with SingleStoreDB Cloud, install the Datadog SingleStore integration and then configure it in the [Cloud Portal][1]. 

## Setup

Start the configuration process from Datadog and complete the configuration in the SingleStore Cloud Portal:

1. [Install the SingleStoreDB Cloud Integration in Datadog](#install-the-singlestoredb-cloud-integration-in-datadog)
2. [Configure the Datadog Integration in the Cloud Portal](#configure-the-datadog-integration-in-the-cloud-portal)

### Install the SingleStoreDB Cloud integration in Datadog

1. Navigate to the [SingleStoreDB Cloud][4] integration tile in Datadog.
3. Select **Install Integration** and wait for installation to complete before proceeding.
4. On the **Configure** tab, select **Connect Accounts**. This action takes you to the [Cloud Portal][1].

The steps above only need to be performed once to connect your first workspace group with Datadog. Once the integration is installed and the accounts are connected, follow the steps specified under [Configure the Datadog Integration in the Cloud Portal](#configure-the-datadog-integration-in-the-cloud-portal) to connect consecutive workspace groups. 

### Configure the Datadog integration in the Cloud Portal

To connect your SingleStoreDB Cloud workspace group with Datadog:

1. Sign in to the Cloud Portal. Upon signing in, you are taken to the **Integration** page. You can also select **Monitoring > Integration** on the left navigation pane to access this page.
2. From the list of available integrations, select **+ Integration** for Datadog.
3. On the **Create Datadog Integration** dialog, from the **Workspace Group** list, select your workspace group.
4. Select **Create**. This action takes you to the Datadog sign-in page. After signing in to Datadog, proceed to the next step.
5. On the **Authorize access** screen, select the **Authorize** button. Upon successful authorization, you are taken to the **Integration** page on the Cloud Portal. 

You can now monitor your SingleStoreDB Cloud databases using Datadog.

### Uninstall the Datadog integration

Follow these steps to uninstall the Datadog integration:

1. **Uninstall the SingleStoreDB Cloud integration on Datadog**: On the Datadog dashboard, select **Integrations > SingleStoreDB Cloud > Configure > Uninstall Integration**. Once this integration is uninstalled, all previous authorizations are revoked.
2. **Remove the Datadog integration on the Cloud Portal**: On the Cloud Portal, go to **Monitoring > Integration**. Select **Delete** for each Datadog configuration you want to remove. 

Additionally, remove all the API keys associated with this integration.

To stop monitoring a specific workspace group (and retain the integration), navigate to the SingleStore DB Cloud Portal and select **Delete** (**Cloud Portal > Monitoring > Integration**) to remove the Datadog configuration for this workspace group.

## Data Collected

### Metrics

See [metadata.csv][2] for a list of metrics provided by this integration.

### Service Checks

SingleStoreDB Cloud does not include any service checks. 

### Events

SingleStoreDB Cloud does not include any events. 

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://portal.singlestore.com
[2]: https://github.com/DataDog/integrations-extras/blob/master/singlestoredb_cloud/metadata.csv
[3]: https://docs.datadoghq.com/help/

