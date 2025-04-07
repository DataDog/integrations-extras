# Cypress Integration

## Overview

With the Datadog [Cypress integration][1], monitor the performance of your CI/CD pipelines and Cypress tests running in your pipelines by:

- Investigating flaky or failing tests and honing in on failing steps
- Looking at test results with distributed tracing details to comprehend why your Cypress tests are slow     
- Troubleshooting performance gaps in your end-to-end Cypress tests with data collected from RUM & Session Replay
- Monitoring, capturing, and visually replaying real user sessions


## Setup

For more information about integrating Cypress tests with RUM & Session Replay, see the [CI Visibility-RUM integration documentation][2].


### Collect RUM events 

To start collecting Real User Monitoring events from your application, see [Cypress Monitoring][3]. 

### Collect traces 

Your application automatically sends traces to Datadog.

## Data Collected

### Metrics

The CI Visibility-RUM integration does not include any metrics. To generate custom metrics from your RUM application, see [Generate Metrics][4].

### Service Checks 

The Cypress integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog Support][5]. 

## Further Reading 

Additional helpful documentation, links, and articles: 

- [CI Visibility][6]



[1]: /integrations/rum-cypress 
[2]: https://docs.datadoghq.com/continuous_integration/guides/rum_integration/
[3]: https://docs.datadoghq.com/continuous_integration/guides/rum_integration/#browser-tests-and-rum
[4]: https://docs.datadoghq.com/real_user_monitoring/generate_metrics 
[5]: https://docs.datadoghq.com/help/
[6]: https://docs.datadoghq.com/continuous_integration/
