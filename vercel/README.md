# Vercel

![datadog-integration][1]

## Overview

[Vercel][2] is a deployment and collaboration platform that enables frontend developers to build high-performance websites and applications. Vercel is also the creator of Next.js, a React framework developed in collaboration with engineers at Google and Facebook in 2016. Vercel users can leverage a built-in deployment tool that manages the build and rendering process, as well as a proprietary [Edge Network][3] that caches their sites for fast retrieval. Additionally, Vercel offers [Serverless Functions][4], which allow users to deploy serverless code to accomplish essential backend processes like user authentication, form submission, and database queries.

Integrate Vercel with Datadog to:

- View and parse your application logs using [Datadog's Log Management][5]
- See the number of requests and 4xx/5xx HTTP errors to your serverless applications and APIs running on Vercel
- Monitor frontend and [Vercel Functions][9] performance with [Datadog Synthetics][6]

## Setup

- [Configure the Vercel integration][7]

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

Need help? Contact [Datadog support][8].

## Further Reading

{{< partial name="whats-next/whats-next.html" >}}

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/vercel/images/logo-full-black.png
[2]: https://vercel.com/
[3]: https://vercel.com/docs/edge-network/overview
[4]: https://vercel.com/docs/serverless-functions/introduction
[5]: /logs/
[6]: /synthetics/
[7]: https://app.datadoghq.com/setup/vercel
[8]: /help/
[9]: https://vercel.com/docs/functions
[10]: https://vercel.com/docs/observability/log-drains
[11]: https://github.com/DataDog/integrations-extras/blob/master/vercel/metadata.csv
