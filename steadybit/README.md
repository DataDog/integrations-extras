# Steadybit

## Overview

[Steadybit][1] is a chaos engineering platform allowing you to simulate turbulent conditions in a controlled way, to improve system reliability and guide your organization to better incident management.

Through this integration, you can leverage Datadog information within chaos-engineering experiments and see chaos-engineering activity in the form of events within Datadog.

## Setup

The integration between Datadog and Steadybit is done through the [Steadybit Datadog extension][2]. The extension interacts with Datadog's API to gather information about monitors and report events to Datadog.

### Prerequisites

You need a [free or paid Steadybit license][3]. The integration supports Steadybit's SAAS and on-premises offering.

### Installation

Several [installation methods are supported][4]. For the best experience, install the Steadybit Datadog extension through the dedicated Helm chart.

To learn more about the supported values for `datadog.siteParameter` and `datadog.siteUrl`, see the [Datadog sites][5] page.

```
helm repo add steadybit https://steadybit.github.io/helm-charts
helm repo update

helm upgrade steadybit-extension-datadog \
  --install \
  --wait \
  --timeout 5m0s \
  --create-namespace \
  --namespace steadybit-extension \
  --set datadog.apiKey="{{API_KEY}}" \
  --set datadog.applicationKey="{{APPLICATION_KEY}}" \
  --set datadog.siteParameter="{{SITE_PARAMETER}}" \
  --set datadog.siteUrl="{{SITE_URL}}" \
  steadybit/steadybit-extension-datadog
```

### Validation

Once the Steadybit Datadog extension is running, see a list of Datadog monitors within the *Landscape* tab in Steadybit.

## Data Collected

### Metrics

Steadybit does not include any metrics.

### Service Checks

Steadybit does not include any service checks.

### Events

Steadybit reports events to Datadog indicating chaos engineering activity. All such events carry the `source:steadybit` tag.

## Troubleshooting

Need help? Contact [Steadybit's support](mailto:support@steadybit.com).

[1]: https://steadybit.com/?utm_campaign=datadogintegration&utm_source=datadog&utm_medium=integration-readme
[2]: https://hub.steadybit.com/extension/com.github.steadybit.extension_datadog?utm_campaign=datadogintegration&utm_source=datadog&utm_medium=integration-readme
[3]: https://signup.steadybit.io/?utm_campaign=datadogintegration&utm_source=datadog&utm_medium=integration-readme
[4]: https://hub.steadybit.com/extension/com.github.steadybit.extension_datadog?utm_campaign=datadogintegration&utm_source=datadog&utm_medium=integration-readme#content-installation
[5]: https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site
