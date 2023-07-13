# Shipyard

## Overview

Shipyard enables teams with on-demand (ephemeral) environments on every code change (PR). We lower teams preproduction cloud costs by 70%, increase developer velocity by 50%, and give DevOps/SRE ~30% of their week back!  Shipyard works in your existing CI workflow, empowering teams to test before they merge.

The Datadog Shipyard integration automatically passes your [Shipyard][1] ephemeral environment logs to Datadog for all applications on which you have enabled Datadog logging.

This is useful for: 

- Monitoring your application's runtime status
- Using Datadog to enrich and parse your runtime logs
- Uncovering trends and comparing the logs from your application's environments to the rest of your Datadog data

## Setup

These instructions assume you have a Shipyard account. If you do not, you can get started [for free][2].

### Configuration

1. Navigate to the [API Keys page][5] and create an API key.
2. In your Shipyard dashboard, go to **Settings**. 
3. Under the Datadog section, enter your Datadog API key and the Datadog site URL.
   ![datadog-input][6]
   1. If you do not see a Datadog section here, email [Shipyard support][3] to enable this feature for your organization.
   2. To get your Datadog site URL, see [Getting Started with Datadog Sites][4].
4. Click **Install Datadog**.
   1. *(Optional)* Toggle `enable Datadog logging for all environments` if you would like Shipyard to automatically send logs for **all** of your environments.
5. To enable Datadog logging for select environments, see the [Configure Application page][10]. 
   1. Select the **Notification and General Settings** tab. 
   2. Toggle `Enable Datadog logging for this environment`.

For more information about setting up the Datadog Shipyard integration, see the [Shipyard documentation][7]. 

## Data Collected

### Metrics

Shipyard does not include any metrics.

### Service Checks

Shipyard does not include any service checks.

### Events

Shipyard does not include any events.

## Troubleshooting

Need help? Contact [Shipyard support][3].

[1]: https://shipyard.build/
[2]: https://shipyard.build/signup
[3]: mailto:support@shipyard.build
[4]: https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: https://raw.githubusercontent.com/mesmith027/DataDog-integrations-extras/shipyard-integration/shipyard/images/datadog-input.png
[7]: https://docs.shipyard.build/docs/integrations/#send-logs-to-datadog
[8]: https://www.datadoghq.com/solutions/log-analysis-and-correlation/
[9]: https://www.datadoghq.com/solutions/shift-left-testing/
[10]: https://docs.shipyard.build/docs/config
