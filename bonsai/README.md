# Bonsai Integration

## Overview

Track request level metrics for your Bonsai clusters to:

- Visualize the performance of your clusters
- Correlate search performance with application performance
- Create alerts

![snapshot][1]

## Setup

Integrating your cluster with Datadog requires submitting your API key to the bonsai app.

### Acquire API key

In Datadog, navigate to [Integrations --> API][2] and copy your API Key.

![snapshot][3]

### Submit API key

Navigate to [Bonsai --> Clusters][4] and click the cluster you want to integrate. Navigate to the Manage tab and scroll to the bottom of the page.

Under the "Datadog Integration" section paste your API key and click "Activate Datadog".

![snapshot][5]

### Verify

If your key is valid, you should see the integration as active.

![snapshot][6]

Within a few minutes, request metrics are available in your Datadog dashboard.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

Metrics are tagged for each cluster, so you can segment based on clusters. The tags look like:

```text
cluster:my-cluster-slug
```

### Events

The Bonsai integration does not include any events.

### Service Checks

The Bonsai integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog Support][8].

## Further Reading

Learn more about infrastructure monitoring and all Datadog integrations in [our blog][9].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bonsai/images/snapshot.png
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bonsai/images/copy_key.png
[4]: https://app.bonsai.io/clusters
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bonsai/images/activate_datadog.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bonsai/images/datadog_activated.png
[7]: https://github.com/DataDog/integrations-extras/blob/master/bonsai/metadata.csv
[8]: https://docs.datadoghq.com/help/
[9]: https://www.datadoghq.com/blog
