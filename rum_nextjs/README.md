# Next.js Integration

## Overview

The Datadog RUM Next.js integration adds App Router support to the Datadog Browser RUM SDK. It automatically tracks route changes and normalizes dynamic route segments into parameterized view names.

**Requirements**: Next.js App Router v15.3+ (uses the [`instrumentation-client`][1] file convention).

## Setup

Start by setting up [Datadog RUM][2] in your Next.js application.

### 1. Create an `instrumentation-client.js` file

Create an `instrumentation-client.js` (or `.ts`) file in the root of your Next.js project and initialize the Datadog RUM SDK with the `nextjsPlugin`:

```javascript
import { datadogRum } from '@datadog/browser-rum'
import { nextjsPlugin } from '@datadog/browser-rum-nextjs'

datadogRum.init({
  applicationId: '<APP_ID>',
  clientToken: '<CLIENT_TOKEN>',
  site: 'datadoghq.com',
  plugins: [nextjsPlugin({ router: 'app' })],
})
```

### 2. Wrap your root layout with the provider

Add `DatadogRumProvider` to your root layout to enable automatic route change tracking:

```tsx
// app/layout.tsx
import { DatadogRumProvider } from '@datadog/browser-rum-nextjs'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <DatadogRumProvider>{children}</DatadogRumProvider>
      </body>
    </html>
  )
}
```

## Route Tracking

The `DatadogRumProvider` automatically tracks route changes and normalizes dynamic segments into parameterized view names:

| Actual URL | View name |
|---|---|
| `/about` | `/about` |
| `/users/123` | `/users/[id]` |
| `/users/123/posts/456` | `/users/[userId]/posts/[postId]` |
| `/docs/a/b/c` | `/docs/[...slug]` |

### Manual view tracking

If you need to start a view manually, use `startNextjsView`:

```javascript
import { startNextjsView } from '@datadog/browser-rum-nextjs'

startNextjsView('/my-custom-view-name')
```

### Custom route name computation

To customize how view names are computed from a pathname and its parameters, use `computeViewNameFromParams`:

```javascript
import { computeViewNameFromParams } from '@datadog/browser-rum-nextjs'

const viewName = computeViewNameFromParams('/users/123', { id: '123' })
// Returns: '/users/[id]'
```


## Go Further with Datadog Next.js Integration

### Traces

Connect your RUM and trace data to get a complete view of your application's performance. See [Connect RUM and Traces][3].

### Logs

To start forwarding your Next.js application's logs to Datadog, see [JavaScript Logs Collection][4].

### Metrics

To generate custom metrics from your RUM application, see [Generate Metrics][5].

## Troubleshooting

Need help? Contact [Datadog Support][6].

## Further Reading

Additional helpful documentation, links, and articles:

- [Next.js Monitoring][7]

[1]: https://nextjs.org/docs/app/api-reference/file-conventions/instrumentation-client
[2]: https://docs.datadoghq.com/real_user_monitoring/browser/setup/client
[3]: https://docs.datadoghq.com/real_user_monitoring/platform/connect_rum_and_traces/?tab=browserrum
[4]: https://docs.datadoghq.com/logs/log_collection/javascript/
[5]: https://docs.datadoghq.com/real_user_monitoring/generate_metrics
[6]: https://docs.datadoghq.com/help/
[7]: https://docs.datadoghq.com/real_user_monitoring/browser/monitoring_page_performance/
