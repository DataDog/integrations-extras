# Agent Check: Statsig

## Overview

The Datadog-Statsig integration enables Statsig to send events and metrics to help you monitor your product and services and visualize how feature gate rollouts or configuration changes affect the rest of your ecosystem.

## Setup

### Installation

No installation is required to setup the Statsig integration.

### Configuration

1. Copy your Datadog API key.
2. [Navigate to the Integrations tab in the Statsig console][1].
3. Click on the Datadog card.
4. Paste in your API key in the top field and click Confirm.

## Data Collected

The Statsig integration does not collect any data from Datadog.

### Metrics

See [metadata.csv][2] for a list of metrics provided by this integration.

### Service Checks

The Statsig integration does not include any service checks.

### Events

The Statsig integration sends configuration change events on Statsig to Datadog. For instance, updated feature gates or new integrations.

## Troubleshooting

Need help? Contact Statsig Support at support@statsig.com or [contact us here][3].

## Further Reading

Additional helpful documentation, links, and articles:

- [Monitor feature releases with Statsig's offering in the Datadog Marketplace][4]

[1]: https://console.statsig.com/integrations
[2]: https://github.com/DataDog/integrations-extras/blob/master/statsig/metadata.csv
[3]: https://www.statsig.com/contact
[4]: https://www.datadoghq.com/blog/feature-monitoring-statsig-datadog-marketplace/
