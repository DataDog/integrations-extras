# 1E

## Overview

The 1E Datadog Integration is an API-based integration that collects metrics from 1E products and forwards them to your Datadog account. You can use these metrics to take advantage of the out-of-the-box dashboard or you can create your own visualizations.

## Setup

### Configuration

Getting set up with the 1E Datadog integration is as simple as emailing a Datadog API key and site to the 1E Support team. There's no further configuration required.

1. Go to your [Datadog Integrations page][1] and click on the 1E tile.

2. Click the **Configuration** tab and click **Install Integration** at the bottom.

3. Go to your [Datadog API Keys Management page][2] and create an API key.

4. Determine your [Datadog site][6] by looking at your browser's address bar:

   - If the domain name is `app.datadoghq.com`, your site is `US`.
   - If the domain name is `app.datadoghq.eu`, your site is `EU`.

5. Send an email to [1E support](mailto:support@1e.com) with the Datadog API key and site to activate your 1E Datadog integration.

6. 1Es team will be in touch once your account has been set up. Once it's been setup, navigate to the [Metrics Explorer][7] within Datadog to see metrics begin to flow in.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this integration.

### Service Checks

The 1E integration does not include any service checks.

### Events

The 1E integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][4] or reach out to [1E Support][5].

[1]: https://app.datadoghq.com/account/settings#integrations
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://github.com/DataDog/integrations-extras/blob/master/1e/metadata.csv
[4]: https://docs.datadoghq.com/help/
[5]: https://www.1e.com/
[6]: https://docs.datadoghq.com/getting_started/site/
[7]: https://docs.datadoghq.com/metrics/explorer/
