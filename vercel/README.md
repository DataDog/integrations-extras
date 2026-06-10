# Vercel

![datadog-integration][1]

## Overview

[Vercel][2] is a deployment and collaboration platform that enables frontend developers to build high-performance websites and applications. Vercel is also the creator of Next.js, a React framework developed in collaboration with engineers at Google and Facebook in 2016. Vercel users can leverage a built-in deployment tool that manages the build and rendering process, as well as a proprietary [Edge Network][3] that caches their sites for fast retrieval. Additionally, Vercel offers [Serverless Functions][4], which allow users to deploy serverless code to accomplish essential backend processes like user authentication, form submission, and database queries.

Integrate Vercel with Datadog to:

- View and parse your application logs using [Datadog's Log Management][5]
- See the number of requests and 4xx/5xx HTTP errors to your serverless applications and APIs running on Vercel
- Monitor frontend and [Vercel Functions][9] performance with [Datadog Synthetics][6]
- Trace requests across your Vercel Functions with [Datadog APM][14]

## Setup

The Datadog integration for Vercel is installed from the Vercel Marketplace.

### Install Datadog from the Vercel Marketplace

1. Sign in to Vercel, then open the [Datadog listing in the Vercel Marketplace][7] and select **Connect Account**.

2. Select the Vercel team in which you want to install the integration.

3. Select which projects to monitor: either all projects or a specific subset.

4. Select **Connect Account**. After Vercel provisions the integration, you are redirected to the **Configure Vercel for Serverless** page in Datadog.

### Configure the integration

On the **Configure Vercel for Serverless** page, complete the following steps:

1. **Confirm your organization** - If you belong to multiple Datadog organizations, select which one to connect to your Vercel account.

2. **Select API Key** - Select **Create New** to create a dedicated key for this integration, or choose an existing API key.

3. **Enable Vercel Log Drain for Log Management** - Toggle **Log Drain** on to forward logs from your Vercel apps to Datadog. Set the sampling percentage (1-100%) for the share of logs to forward.

4. **Set Log Sources** - Select which Vercel log sources to forward. At least one is required:
   - **Static**: CDN and static asset request logs
   - **Lambda**: Serverless Function execution logs
   - **Build**: Build output logs
   - **Edge**: Edge Function and Edge Middleware logs
   - **External**: Logs from external services routed through Vercel
   - **Firewall**: Vercel Firewall event logs

   **Note:** To ensure metrics are collected, Datadog recommends enabling **Lambda** logs and **Static** logs. Enabling **Build** logs is recommended if you want to collect build metrics.

5. **Set Log Environment** - Select **Production**, **Preview**, or both. At least one is required.

6. **Enable Vercel Trace Drain for APM** - Toggle **Trace Drain** on to forward traces from your Vercel apps to Datadog. Set the sampling percentage (1-100%).

7. Select **Add Integration**. The **Vercel Integration Setup** status page opens and confirms that data is flowing into Datadog. From there you can navigate to the Vercel Monitoring summary, the out-of-the-box dashboard, the Log Explorer, the Trace Explorer, and Real User Monitoring.

**Note:** Vercel Log Drains and Trace Drains are billed by Vercel. See the Vercel documentation for [Log Drains][10] and [Trace Drains][13].

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this integration.

### Service Checks

The Vercel integration does not include any service checks.

### Events

The Vercel integration does not include any events.

### Logs

The Vercel integration collects logs from your Vercel Project using Vercel's [Log Drains][10] feature.

### Traces

The Vercel integration collects traces from your Vercel Project using Vercel's [Trace Drains][13] feature.

## Troubleshooting

If you are using the [Vercel OpenTelemetry SDK][12], the `serviceName` specified in `registerOTel` block of your initializer must match the Vercel Project name. This enables traces to appear in Datadog with the appropriate logs and metrics.

Need help? Contact [Datadog support][8].

## Further Reading

{{< partial name="whats-next/whats-next.html" >}}

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vercel/images/logo-full-black.png
[2]: https://vercel.com/
[3]: https://vercel.com/docs/edge-network/overview
[4]: https://vercel.com/docs/serverless-functions/introduction
[5]: https://docs.datadoghq.com/logs/
[6]: https://docs.datadoghq.com/synthetics/
[7]: https://vercel.com/marketplace/datadog
[8]: https://docs.datadoghq.com/help/
[9]: https://vercel.com/docs/functions
[10]: https://vercel.com/docs/drains/reference/logs
[11]: https://github.com/DataDog/integrations-extras/blob/master/vercel/metadata.csv
[12]: https://vercel.com/docs/tracing/instrumentation
[13]: https://vercel.com/docs/drains/reference/traces
[14]: https://docs.datadoghq.com/tracing/
