# React Integration

## Overview

With the Datadog RUM React integration, resolve performance issues quickly in React components by:

- Debugging the root cause of performance bottlenecks, such as a slow server response time, render-blocking resource, or an error inside a component
- Automatically correlating web performance data with user journeys, HTTP calls, and logs
- Alerting your engineering teams when crucial web performance metrics (such as Core Web Vitals) fall below a threshold that results in a poor user experience

Monitor your React applications from end-to-end by:

- Tracking and visualizing user journeys across your entire stack
- Debugging the root cause of slow load times, which may be an issue with your React code, network performance, or underlying infrastructure
- Analyzing and contextualizing every user session with attributes such as user ID, email, name, and more
- Unifying full-stack monitoring in one platform for frontend and backend development teams

## Setup

Start by setting up [Datadog RUM][1] in your React application. If you're creating a new RUM application in the Datadog App, select React as the application type. If you already have an existing RUM application, you can update its type to React instead. Once configured, the Datadog App will provide instructions for integrating the [RUM-React plugin][2] with the Browser SDK.

## Error Tracking

To track React component rendering errors, use one of the following:

- An `ErrorBoundary` component (see [React documentation][3]) that catches errors and reports them to Datadog.
- A function that you can use to report errors from your own `ErrorBoundary` component.

#### `ErrorBoundary` usage

```javascript
import { ErrorBoundary } from '@datadog/browser-rum-react'

function App() {
  return (
    <ErrorBoundary fallback={ErrorFallback}>
      <MyComponent />
    </ErrorBoundary>
  )
}

function ErrorFallback({ resetError, error }) {
  return (
    <p>
      Oops, something went wrong! <strong>{String(error)}</strong> <button onClick={resetError}>Retry</button>
    </p>
  )
}
```

### Reporting React errors from your own `ErrorBoundary`

```javascript
import { addReactError } from '@datadog/browser-rum-react'

class MyErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    addReactError(error, errorInfo)
  }

  render() {
    ...
  }
}
```

## React Router integration

`react-router` v6 allows you to declare routes using the following methods:

- Create routers with [`createMemoryRouter`][4], [`createHashRouter`][5], or [`createBrowserRouter`][6] functions.
- Use the [`useRoutes`][7] hook.
- Use the [`Routes`][8] component.

To track route changes with the Datadog RUM Browser SDK, first initialize the `reactPlugin` with the `router: true` option, then replace those functions with their equivalent from `@datadog/browser-rum-react/react-router-v6`. Example:

```javascript
import { RouterProvider } from 'react-router-dom'
import { datadogRum } from '@datadog/browser-rum'
import { reactPlugin } from '@datadog/browser-rum-react'
// Use "createBrowserRouter" from @datadog/browser-rum-react/react-router-v6 instead of react-router-dom:
import { createBrowserRouter } from '@datadog/browser-rum-react/react-router-v6'

datadogRum.init({
  ...
  plugins: [reactPlugin({ router: true })],
})

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    ...
  },
])

ReactDOM.createRoot(document.getElementById('root')).render(<RouterProvider router={router} />)
```

## Go further with Datadog React integration

### Traces

Connect your RUM and trace data to get a complete view of your application's performance. See [Connect RUM and Traces][9].

### Logs

To start forwarding your React application's logs to Datadog, see [JavaScript Logs Collection][10].

### Metrics

To generate custom metrics from your RUM application, see [Generate Metrics][11].

## Troubleshooting

Need help? Contact [Datadog Support][12].

## Further Reading

Additional helpful documentation, links, and articles:

- [React Monitoring][13]

[1]: https://docs.datadoghq.com/real_user_monitoring/browser/setup/client
[2]: https://www.npmjs.com/package/@datadog/browser-rum-react
[3]: https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary
[4]: https://reactrouter.com/en/main/routers/create-memory-router
[5]: https://reactrouter.com/en/main/routers/create-hash-router
[6]: https://reactrouter.com/en/main/routers/create-browser-router
[7]: https://reactrouter.com/en/main/hooks/use-routes
[8]: https://reactrouter.com/en/main/components/routes
[9]: https://docs.datadoghq.com/real_user_monitoring/platform/connect_rum_and_traces/?tab=browserrum
[10]: https://docs.datadoghq.com/logs/log_collection/javascript/
[11]: https://docs.datadoghq.com/real_user_monitoring/generate_metrics
[12]: https://docs.datadoghq.com/help/
[13]: https://www.datadoghq.com/blog/datadog-rum-react-components/
