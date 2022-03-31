# Komodor - Kubernetes Troubleshooting Platform

## Overview

This integration allows Datadog Monitor Alerts to be available in the Komodor Kubernetes troubleshooting platform and to suggest related services based on service connections detected by Datadog.

Komodor tracks changes across your entire K8s stack, analyzes their ripple effect, and provides you with the context you need to troubleshoot efficiently and independently. Komodor gives you insight into your Kubernetes deployments on a timeline with the relevant information like what changed, what code was pushed and by who. You can also view data from your Git, config maps, infrastruture, alerting and other tooling such as Datadog, in one centralized and easy-to-understand display, easily link to Datadog metrics with dynamic deployment links that take you directly to the matrices you need. This allows you to troubleshoot your microservices based on the most relevant context, connections and service dependencies detected in Datadog.

## Setup

Once logged into the Komodor platform, you can easily install our pod-based agent on each Kubernetes cluster by using a Helm chart or Kustomize - here is a [quick overview][2] of installing the agent.

3. Once the agent is installed, set up the Datadog integrations listed below:
    - [Komodor platform integration][3] -  This initial integration allows Datadog Monitor Alerts to be available in Komodor and will suggest related services based on service dependencies detected in Datadog. 
    - [Datadog Webhook Integration][4] - This integrations allows Komodor to receive alerts from Datadog Monitors. You will see all alerts in the Komodor Service View.
    - Datadog Monitor Notification - Adding a Komodor [dynamic link][5] to Datadog Monitor Notifications will generate a direct link to the relevant service in Komodor. You will see the alert link in your Alerting provider connected to Datadog.
4. Once you set up the integrations, enrich the Komodor service and deployment screens by adding links to relevant Datadog APM Dashboards as well as dynamic links to specific service metrics and time ranges within Datadog. This can be done easily with Kubernetes [annotations][6].

### Datadog integration
Komodor supports three types of integrations with Datadog.

#### Komodor platform integration 
This [initial integration][3] allows Datadog Monitor Alerts to be available in Komodor and will suggest related services based on service dependencies detected in Datadog. 

#### Datadog Webhook Integration
The Datadog [Webhook integration][4] allows Komodor to receive alerts from Datadog Monitors. You will see all alerts in the Komodor Service View.

#### Datadog Monitor Notification
Adding a Komodor [dynamic link][5] to Datadog Monitor Notifications will generate a direct link to the relevant service in Komodor. You will see the alert link in your Alerting provider connected to Datadog.

### Configure service and deployment annotations
Enrich the Komodor service and deployment screens by adding links to relevant Datadog APM Dashboards as well as dynamic links to specific service metrics and time ranges within Datadog. This can be done easily with Kubernetes [annotations][6].

## Data Collected

### Log collection
Komodor does not send any logs to Datadog.

### Metrics
Komodor does not include any metrics.

### Service Checks
Komodor does not include any service checks.

### Events
Komodor will display Datadog events in the Komodor Service and Events timelines.

## Support

For more information please [visit our website][1] or contact us at [].

[1]: https://komodor.com/sign-up/
[2]: https://docs.komodor.com/Learn/Komodor-Agent.html
[3]: https://docs.komodor.com/Integrations/Datadog.html
[4]: https://docs.komodor.com/Integrations/datadog-webhook.html
[5]: https://docs.komodor.com/Integrations/Datadog-Monitor-Notification.html
[6]: https://docs.komodor.com/Learn/Annotations.html