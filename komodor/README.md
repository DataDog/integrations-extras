# Komodor - Kubernetes Troubleshooting Platform

## Overview

This integration allows Datadog Monitor Alerts to be available in the Komodor Kubernetes troubleshooting platform and to suggest related services based on service connections detected by Datadog.

Komodor tracks changes across your entire K8s stack, analyzes their ripple effect and provides you with the context you need to troubleshoot efficiently and independently.

### Empower on-call teams
Make the knowledge and expertise that has traditionally been held by only a few, clear and visible to developers, SRE and support teams.

### Understand your kubernetes
Gain the K8s visibility you are lacking. See your deployments on a timeline with the relevant information: what changed, what code was pushed and by whom.

### Track your system end-to-end
View data from your Git, config, infra, alerting and other tools, in one centralized and easy-to-understand display, easily link to Datadog metrics with dynamic deployment links that take you directly to the data you need.

### Uncovering the context
Troubleshoot your microservices based on the most relevant context, connections and dependencies.

### Increase performance and availability
Detect and resolve issues to prevent escalation. Enable any on-call developer to quickly uncover root causes and get the right teams involved for rapid resolution.

## Setup

Once logged into the Komodor platform, you can easily install our pod-based agent on each Kubernetes cluster by using a Helm chart or Kustomize - here is a [quick overview][2] of installing the agent.

Once the agent is installed you can begin setting up the Datadog integrations listed below. Once setup is completed, you can enrich deployment and service metadata with dynamic links and annotations as described below.

### Datadog integration
Komodor supports three types of integrations with Datadog.

#### Komodor platform integration 
This [initial integration][3] will allow Datadog Monitor Alerts to be available in Komodor and will suggest related services based on service dependencies detected in Datadog. 

#### Datadog Webhook Integration
The Datadog [Webhook integration][4] allows Komodor to receive alerts from Datadog Monitors. You will see all alerts in the Komodor Service View.

#### Datadog Monitor Notification
Adding a Komodor [dynamic link][5] to Datadog Monitor Notifications will generate a direct link to the relevant service in Komodor. You will see the alert link in your Alerting provider connected to Datadog.

### Configure service and deployment annotations
Enrich the Komodor service and deployment screens by adding links back to relevant Datadog APM Dashboards and dynamic links that will deep link back to specific service metrics and time ranges within Datadog. This can easily be done by using Kubernetes [annotations][6].

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