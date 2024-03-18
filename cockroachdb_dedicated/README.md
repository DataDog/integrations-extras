# Cockroach Cloud
 
## Overview

The CockroachDB Cloud integration for Datadog enables data collection and alerting on a subset of CockroachDB metrics using the Datadog platform. For more context, go to [CockroachDB Essential Metrics][1].

**NOTE**: link for Essential Metrics Standard does NOT exist yet in public docs

## Setup
 
### Installation
 
To enable Datadog monitoring for a Cockroach Cloud cluster:

1. On the cluster's **Monitoring** > [**Tools** page][14].

2. Fill in the **API key** and **Datadog Site** fields with the corresponding values.
    - The **API key** is associated with your Datadog organization. If you don't have an API key to use with your Cockroach Cloud cluster, you need to create one. For instructions, see the [Datadog documentation][2].
    - Your **Datadog Site** corresponds to your Datadog Site URL. For more details, see the [Datadog documentation][3].

3. Click **Create**.  Depending on the size of your cluster and the current load on the system, the integration might take some time to become enabled.

4. Once it is registered on Datadog, the cluster will appear on your Datadog [Infrastructure List][4]. This can take up to several minutes.
 
### Configuration
 
Open your Datadog [Dashboard List][5]. There are two out of the box dashboards that present CockroachDB metrics
- CockroachDB Cloud Serverless (Limited Preview)
- CockroachDB Cloud Dedicated

To create your own Cockroach Cloud dashboard, you can either [clone][6] the default `CockroachDB Cloud Dedicated` dashboard and edit the widgets, or [create a new dashboard][7].

The [available metrics][8] are intended for use as building blocks for your own charts.

To preview the metrics being collected, you can:

- Click on your cluster's entry in the [Infrastructure List][4] to display time-series graphs for each available metric.
- Use the [Metrics Explorer][9] to search for and view `crdb_cloud` or `crdb_dedicated` metrics.
 
### Validation
 
Once enabled, the **Integration status** in the **Datadog** panel on the **Monitoring** page will show as `Active`.

If an issue is encountered during the integration, one of the following statuses may appear instead:
- `Active` indicates that the integration has been successfully deployed.
- `Inactive` indicates that the integration has not been successfully deployed. Setup has either not been attempted or has encountered an error.
- `Unhealthy` indicates that the integration API key is invalid and needs to be [updated](#update-integration).
- `Unknown` indicates that an unknown error has occurred. If this status is displayed, [contact our support team][10].

Metrics export from CockroachDB can be interrupted in the event of:

- A stale API key. In this case, the integration status will be `Unhealthy`. To resolve the issue, [update your integration](#update-integration) with a new API key.
- Transient CockroachDB unavailbility. In this case, the integration status will continue to be `Active`. To resolve the issue, try [deactivating](#deactivate-integration) and reactivating the integration from the **Datadog** panel. If this does not resolve the issue, [contact our support team][10].

To monitor the health of metrics export, you can create a custom Monitor in Datadog. 

### Update integration

To update the metadata associated with the integration (for example, to rotate API keys):

1. In the **Datadog** panel, click the ellipsis and select **Update**.

1. Update the **API key** and **Datadog Site** fields and click **Create**. The integration will be redeployed. 

### Deactivate integration

To deactivate the integration:

1. In the **Datadog** panel, click the ellipsis and select **Deactivate integration**.

1. When disabled, the **Integration status** in the panel will show as `Inactive`.

After deactivating an integration, the metrics data will remain in Datadog for a default [retention period][11]. 

## Data Collected

### Metrics

- `crdb_cloud` & `crdb_dedicated` [Metrics][13]

### Service Checks

The Cockroach Cloud integration does not include any service checks.

### Events

The Cockroach Cloud integration does not include any events.
 
## Support
 
Need help? Contact [Datadog support][12].


[1]: https://www.cockroachlabs.com/docs/cockroachcloud/essential-metrics
[2]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[3]: https://docs.datadoghq.com/getting_started/site/
[4]: https://docs.datadoghq.com/infrastructure/list/
[5]: https://docs.datadoghq.com/dashboards/#dashboard-list
[6]: https://docs.datadoghq.com/dashboards/#clone-dashboard
[7]: https://docs.datadoghq.com/dashboards/#new-dashboard
[8]: https://docs.datadoghq.com/integrations/cockroachdb_dedicated/#data-collected
[9]: https://docs.datadoghq.com/metrics/explorer/
[10]: https://support.cockroachlabs.com/
[11]: https://docs.datadoghq.com/developers/guide/data-collection-resolution-retention/
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/cockroachdb_dedicated/metadata.csv
[14]: https://www.cockroachlabs.com/docs/cockroachcloud/tools-page
