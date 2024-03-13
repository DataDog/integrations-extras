# Split

## Overview

[Split][1] is a platform for [controlled rollouts][2], helping businesses of all sizes deliver exceptional user experiences and mitigate risk by providing an easy, secure way to target features to customers.

Integrate Split with Datadog to:

- See feature changes in context by including Split changelogs in your event stream
- Correlate feature impact with application performance
- Avoid critical issues before they happen. Disable features proactively based on Datadog metrics and alerts

To enrich Real User Monitoring (RUM) data with your Split feature flags for visibility into performance and behavioral changes, see the [Split-RUM integration page][8].

## Setup

- **In Datadog**: Create an API Key <span class="hidden-api-key">\${api_key}</span>

- **In Split**: Go to **Admin Settings** and click **Integrations** and navigate to the Marketplace. Click Add next to Datadog.<br/>

![Split Screenshot][3]

- Paste your Datadog API Key and click Save.

![Split Screenshot][4]

Split data should be flowing into Datadog.

### Feature Flag Tracking integration

See the [Split-RUM integration page][8] for information about setting up feature flag tracking with the RUM Browser SDK.

## Data Collected

### Metrics

The Split check does not include any metrics.

### Events

Push your Split listing/de-listing events into your [Datadog Event Stream][5].

### Service Checks

The Split check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: http://www.split.io
[2]: http://www.split.io/articles/controlled-rollout
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/split/images/in-split.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/split/images/integrations-datadog.png
[5]: https://docs.datadoghq.com/events/
[6]: https://docs.datadoghq.com/help/
[7]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
[8]: https://docs.datadoghq.com/integrations/split-rum/