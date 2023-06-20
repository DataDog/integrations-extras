# React Integration

## Overview

With the Datadog [React integration][1], resolve performance issues quickly in React components by:

- Debugging the root cause of performance bottlenecks, such as a slow server response time, render-blocking resource, or an error inside a component
- Automatically correlating React performance data with user journeys, AJAX calls to the server side, and logs
- Alerting your engineering teams when crucial performance metrics for React (such as Core Web Vitals) fall below a threshold that results in a poor user experience


Monitor your React applications from end-to-end by:

- Tracking and visualizing user journeys across your entire stack
- Debugging the root cause of slow load times, which may be an issue with your React code, network performance, or underlying infrastructure 
- Analyzing and contextualizing every user session with attributes such as user ID, email, name, and more
- Unifying full-stack monitoring in one platform for frontend and backend development teams

## Setup

### Collect RUM events 

To start collecting Real User Monitoring events from your React application, see [React Monitoring][2].

### Collect traces 

Your React application automatically sends traces to Datadog.

### Collect logs 

To start forwarding your React application's logs to Datadog, see [React Log Collection][3].

## Data Collected

### Metrics

The React integration does not include any metrics. To generate custom metrics from your RUM application, see [Generate Metrics][4].

### Events 

For more information about events and attributes, see [RUM React Data Collected][5]. 

### Service Checks 

The React integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog Support][6]. 

## Further Reading 

Additional helpful documentation, links, and articles: 

- [React Monitoring][7]



[1]: https://app.datadoghq.com/integrations/rum-react 
[2]: https://docs.datadoghq.com/real_user_monitoring/browser/ 
[3]: https://docs.datadoghq.com/logs/log_collection/javascript/
[4]: https://docs.datadoghq.com/real_user_monitoring/generate_metrics
[5]: https://docs.datadoghq.com/real_user_monitoring/browser/data_collected/
[6]: https://docs.datadoghq.com/help/ 
[7]: https://www.datadoghq.com/blog/datadog-rum-react-components/

