# Steadybit

## Overview

[Steadybit](https://steadybit.com/) is the first reliability engineering platform to go beyond Chaos Engineering. Organizations in the eCommerce, SaaS and financial services industries, as well as global enterprises choose Steadybit to roll out chaos engineering across their teams to foster a culture of reliability. Steadybit provides everything an organization needs to make it safe and easy to bridge the gap between the experts (SREs, platform and expert teams) and the developers.

The monitor status check step can be dragged&dropped into the experiment editor. Once done, you can use it to collect information about the state of the Datadog monitors and, optionally, to verify that they are within the expected status.

Experiments can be aborted and marked as failed when the Datadog monitor status check's actual state diverges from the expected state. This helps implement pre-/post-conditions and invariants. For example, to only start an experiment when the system is healthy.


## Setup

The integration between Datadog and Steadybit is done through the [Steadybit Datadog extension][2]. The extension interacts with Datadog's API to gather information about monitors and report events to Datadog.

### Prerequisites

You will need a [free or paid Steadybit license][3]. The integration supports Steadybit's SAAS and on-premises offering.

### Installation

Several [installation methods are supported][4]. The simplest way to install the Steadybit Datadog extension is through our dedicated Helm chart.

To learn more about the supported values for `datadog.siteParameter` and `datadog.siteUrl`, please see [Datadog's site documentation page][5].

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

Once the Steadybit Datadog extension is running, you can see a list of Datadog monitors within the *Landscape* tab in Steadybit.

## Data Collected

### Metrics

Steadybit does not include any metrics.

### Service Checks

Steadybit does not include any service checks.

### Events

Steadybit reports events to Datadog indicating chaos engineering activity. All such events carry the `source:steadybit` tag.

## Troubleshooting

Need help? Contact [Steadybit's support](mailto:support@steadybit.com).
