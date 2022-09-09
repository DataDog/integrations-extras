# unitQ

## Overview

The unitQ Datadog integration allows you to forward metrics from unitQ to Datadog. Datadog supports an advanced function API, which enables you to create graphs and alerts for user feedback metrics.

## Setup

### Configuration

1. In unitQ, go to **Integrations**.
2. Select the Datadog tile
3. Fill in the following details:
   - **Datadog Site**:
     - Enter `https://api.datadoghq.com` if you use the Datadog US region.
     - Enter `https://api.datadoghq.eu` if you use the Datadog EU region.
   - **API Key**: Enter your [Datadog API key][3].

## Data Collected

### Metrics

See [metadata.csv][1] for a list of metrics provided by this integration.

### Service Checks

unitQ does not include any service checks.

### Events

unitQ does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][2].

[1]: https://github.com/DataDog/integrations-extras/blob/master/unitq/metadata.csv
[2]: https://docs.datadoghq.com/help/
[3]: https://app.datadoghq.com/organization-settings/api-keys
