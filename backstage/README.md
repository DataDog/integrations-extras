# Agent Check: backstage

## Overview

[Backstage][1] is an open platform for building Developer Portals. This integration enables you to embed Datadog graphs and dashboards into your Backstage instance.

## Setup

### Installation

1. Install the Datadog plugin into Backstage:

```shell
cd packages/app
yarn add @roadiehq/backstage-plugin-datadog
```

2. Add the Datadog plugin widget to your Backstage Overview tab. See the [detailed instructions][2] for more information.
3. Find or create the [public URL][3] for your Datadog dashboard. 
4. Add the dashboard URL to the plugin's metadata:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: sample-service
  description: |
    A sample service
  annotations:
    datadoghq.com/dashboard-url: <DATADOGURL>
```

### Verifiaction

Open your Backstage instance Overview tab and see if your Datadog dahsboard or graph is rendered as expected.

## Data Collected

### Metrics

The Backstage integration does not include any metrics.

### Service Checks

The Backstage integration does not include any service checks.

### Events

The Backstage integration does not include any events.

## Troubleshooting

Need help? Reach out to the [Backstage Community](https://backstage.io/community).

[1]: https://backstage.io
[2]: https://roadie.io/backstage/plugins/datadog/
[3]: https://docs.datadoghq.com/dashboards/sharing/#share-a-dashboard-by-public-url
[4]: https://raw.githubusercontent.com/RoadieHQ/roadie-backstage-plugins/main/plugins/frontend/backstage-plugin-datadog/docs/datadog-widget.png