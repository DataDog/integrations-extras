# Vercel

![datadog-integration][1]

## Overview

[Vercel][2] is a deployment and collaboration platform that enables frontend developers to build high-performance websites and applications. Vercel is also the creator of Next.js, a React framework developed in collaboration with engineers at Google and Facebook in 2016. Vercel users can leverage a built-in deployment tool that manages the build and rendering process, as well as a proprietary [Edge Network][3] that caches their sites for fast retrieval. Additionally, Vercel offers [Serverless Functions][4], which allow users to deploy serverless code to accomplish essential backend processes like user authentication, form submission, and database queries.

Integrate Vercel with Datadog to:

- View and parse your application logs using [Datadog's Log Management][5]
- See the number of requests and 4xx/5xx HTTP errors to your serverless applications and APIs running on Vercel
- Monitor frontend and [Vercel Functions][9] performance with [Datadog Synthetics][6]

## Setup

### Datadog

To connect Datadog with Vercel, enable the integration and selct an API Key.

1. Open the Vercel integration tile.

2. Select the **Configure** tab and select **Configure the Vercel integration**.

3. On the **Your Datadog account info** form, select **Select an API Key** and either choose an existing API key or select **+ Create New** to use a new API key for the Vercel integration.

4. After your selection is made, select **Use API Key**. This copies the selected API key to your device's clipboard.

5. After the API key is selected, you are redirected back to the **Your Datadog account info** form. Select **Vercel > Add Integration** to complete the integration setup for Vercel.
### Vercel

1. Click the **Vercel > Add Integration** link to be redirected to Vercel's Datadog integration page.

2. Select **Connect Account** to open the **Connect Datadog Account** form.

3. Select which Vercel Team to connect the integration to. (Teams that already have the integration installed have an icon next to them labeled **Installed**)

4. Select the radio button associated with either enabling the integration for all projects or a specific project that the team owns. Select **Connect Account** to save your changes.

5. Paste the API key that was copied to your clipboard in Step 4 of the Datadog setup above into the box labeled **Your Datadog API Key**.

6. Scroll to the bottom of the form and select **Add Integration** to save your changes.

- {{< region-param key="vercel_setup" link="true" text="Configure the Vercel integration" >}}

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Service Checks

The Vercel integration does not include any service checks.

### Events

The Vercel integration does not include any events.

### Logs

The Vercel integration collects logs from your Vercel Project using Vercel's [Log Drains][10] feature.

## Troubleshooting

If you are using the Vercel OpenTelemetry Collector, the `serviceName` specified in `registerOTel` block of your [initializer][12] must match the Vercel Project name. This enables traces to appear in Datadog with the appropriate logs and metrics.


Need help? Contact [Datadog support][8].

## Further Reading

{{< partial name="whats-next/whats-next.html" >}}

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vercel/images/logo-full-black.png
[2]: https://vercel.com/
[3]: https://vercel.com/docs/edge-network/overview
[4]: https://vercel.com/docs/serverless-functions/introduction
[5]: /logs/
[6]: /synthetics/
[8]: /help/
[9]: https://vercel.com/docs/functions
[10]: https://vercel.com/docs/observability/log-drains
[11]: https://github.com/DataDog/integrations-extras/blob/master/vercel/metadata.csv
[12]: https://vercel.com/docs/observability/otel-overview#initialize-otel