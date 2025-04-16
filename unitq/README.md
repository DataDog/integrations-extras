# unitQ

## Overview

unitQ is your consolidated, searchable platform for user feedback. Our AI technology extracts data-driven insights from what users are saying to help you increase product quality.

The unitQ Datadog integration allows you to forward metrics from unitQ to Datadog. By delivering unitQ metrics to Datadog, users can leverage Datadog's graphing and alerting capabilities to track user feedback - ensuring a happy customer base.

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
[3]: /organization-settings/api-keys
