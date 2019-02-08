## Overview

Track request level metrics for your Bonsai clusters to:

* Visualize the performance of your clusters
* Correlate search performance with application performance
* Create alerts

![snapshot](https://raw.githubusercontent.com/omc/IntegrationTemplate/master/Bonsai/images/snapshot.png)

## Setup

Integrating your cluster with Datadog requires submitting your API key to the bonsai app.


### Step 1 - Aquire API Key

Navigate to https://app.datadoghq.com/account/settings#api and copy the API Key

![snapshot](https://raw.githubusercontent.com/omc/IntegrationTemplate/master/Bonsai/images/copy_key.png)


### Step 2 - Submit API Key

Navigate to https://app.bonsai.io/clusters and click the cluster you want to integrate.  Navigate to the Manage tab and scroll to the bottom of the page.

Under the "Datadog Integration" section paste your API key and click "Activate Datadog"

![snapshot](https://raw.githubusercontent.com/omc/IntegrationTemplate/master/Bonsai/images/activate_datadog.png)

### Step 3 - Verify

If your key is valid, you should see the integration as active.

![snapshot](https://raw.githubusercontent.com/omc/IntegrationTemplate/master/Bonsai/images/datadog_activated.png)

Within a few minutes, request metrics are available in your Datadog dashboard.

## Data Collected

### Metrics

See [metadata.csv](https://github.com/omc/IntegrationTemplate/blob/master/Bonsai/metadata.csv) for a list of metrics provided by this integration.

Metrics are tagged for each cluster, so you can segment based on clusters.  The tags look like:

```
cluster:my-cluster-slug
```

### Events

The Bonsai integration does not include any events at this time.

### Service Checks

The Bonsai integration does not include any service checks at this time.

## Troubleshooting

Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).
