# Komodor - Kubernetes Troubleshooting Platform

## Overview

Komodor tracks changes across your entire K8s stack, analyzes their ripple effect, and provides you with the context you need to troubleshoot efficiently and independently. Komodor gives you insight into your Kubernetes deployments on a timeline with relevant information such as what changed, what code was pushed, and who pushed it. You can also view data from Git, config maps, your infrastructure, alerting, and other tools such as Datadog, in one centralized and easy-to-understand display. 
	
With this integration, you can link to Datadog metrics with dynamic deployment links that take you directly to the dashboards you need. This allows you to troubleshoot your microservices based on the most relevant context, connections, and service dependencies detected in Datadog.
	
## Setup
	
1. Log onto the [Komodor platform][7].
2. Install the Komodor pod-based agent on each Kubernetes cluster by using a Helm chart or Kustomize. For more information, see the [Komodor docs][2] for installing the agent.

3. Once the agent is installed, follow the steps below to set up the Datadog integration:
	- Install the [Komodor platform integration][3] - This first integration step allows Komodor to access your Datadog account via API key and Token key, and to suggest related services based on service dependencies detected in Datadog.
	- Install the [Datadog Webhook integration][4] - This allows Komodor to receive alerts from Datadog monitors. You can see all alerts in the Komodor Service View.
	- Configure a Datadog monitor notification - Adding a Komodor [dynamic link][5] to Datadog [monitor notifications][9] generates a direct link to the relevant service in Komodor. See the alert link in your Alerting provider connected to Datadog.
	
4. Use Komodor [annotations][6] to enrich the Komodor service and deployment screens with links to relevant Datadog APM dashboards, as well as dynamic links to specific service metrics and time ranges within Datadog.

## Support

For more information please [visit our website][1] or [contact us][8].

[1]: https://komodor.com/sign-up/
[2]: https://help.komodor.com/hc/en-us/sections/17579101174674-Komodor-Agent
[3]: https://help.komodor.com/hc/en-us/articles/16241138371858-Datadog-Integration
[4]: https://help.komodor.com/hc/en-us/articles/16241177474578-Datadog-Webhook-Integration
[5]: https://help.komodor.com/hc/en-us/articles/16241181517714-Datadog-Monitor-Notifications
[6]: https://help.komodor.com/hc/en-us/articles/16240380547730-Komodor-Custom-3rd-Party-Links
[7]: https://app.komodor.com/
[8]: https://komodor.com/contact-us/
[9]: https://docs.datadoghq.com/monitors/notify/
