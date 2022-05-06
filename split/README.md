# Split

## Overview

[Split][1] is a platform for [controlled rollouts][2], helping businesses of all sizes deliver exceptional user experiences and mitigate risk by providing an easy, secure way to target features to customers.

Integrate Split with Datadog to:

- See feature changes in context by including Split changelogs in your event stream
- Correlate feature impact with application performance
- Avoid critical issues before they happen. Disable features proactively based on Datadog metrics and alerts

## Setup

- **In Datadog**: Create an API Key <span class="hidden-api-key">\${api_key}</span>

- **In Split**: Go to **Admin Settings** and click **Integrations** and navigate to the Marketplace. Click Add next to Datadog.<br/>

![Split Screenshot][3]

- Paste your Datadog API Key and click Save.

![Split Screenshot][4]

Split data should be flowing into Datadog.

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
