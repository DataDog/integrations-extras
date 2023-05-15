## Overview

MongoDB Atlas can push calculated metrics into Datadog to:

- Visualize key MongoDB Atlas metrics.
- Correlate MongoDB Atlas performance with the rest of your applications.

**Note: This integration is only available on M10+ clusters.**

## Setup

### Installation

You can install the MongoDB Atlas integration by logging into your Atlas portal.

### Configuration

1. Retrieve or create a Datadog [API key][1].
2. In the [Atlas portal][2], enter a Datadog API key under **Integrations** -> **Datadog Settings**.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this integration.

### Events

MongoDB Atlas can push [alerts][4] to Datadog as events.

### Service Checks

The MongoDB Atlas integration does not include any service checks.

## Troubleshooting

Need help? [Contact Datadog Support][5]

## Further Reading

{{< partial name="whats-next/whats-next.html" >}}

[1]: https://app.datadoghq.com/organization-settings/api-keys
[2]: https://docs.atlas.mongodb.com/tutorial/monitoring-integrations/#procedure
[3]: https://github.com/DataDog/integrations-extras/blob/master/mongodb_atlas/metadata.csv
[4]: https://www.mongodb.com/blog/post/push-your-mongodb-atlas-alerts-to-datadog
[5]: https://docs.datadoghq.com/help/
