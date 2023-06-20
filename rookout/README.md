# Rookout for Datadog

## Overview

### Description

[Rookout][1] is a disruptive developer solution for cloud native debugging and live data collection. Rookout's Non-Breaking Breakpoints let you collect any type of data on the fly with no extra coding, redeployments, or restarts.

Rookout is designed from the ground up for production environments and modern architecture debugging, such as Kubernetes, microservices, serverless, and service-mesh based applications.

The Rookout integration lets you collect metrics from your code running live in production or any other environment, without ever needing to stop or redeploy it.

### Usage

The Rookout integration has two components:

- A context menu item for your dashboard widgets that lets you collect metric points from your code.
- A custom widget showing you all the metric points you have set in Rookout.

**Context Menu Item**

When clicking on a timeseries widget that represents one or more servers or services, a new context menu item appears.

Clicking on "Set metric points" opens the Rookout app, and automatically selects the correct instances for you.

**Custom Dashboard Widget**

Add the Rookout widget to your dashboard to see where you have set metric points.

## Setup

### Configuration

To add the Rookout context menu item to a timeseries widget in your dashboard, you need to add a rookout label filter to its title.

For instance, if a timeseries shows some metric in a service called `cartservice`, you want the Rookout context menu item to automatically start a Rookout session with the label filter: `k8s_deployment:cartservice`.

To do that, add `[k8s_deployment:cartservice]` to the title of the timeseries widget.

## Data Collected

### Metrics

Rookout does not include any metrics.

### Service Checks

Rookout does not include any service checks.

### Events

Rookout does not include any events.

## Troubleshooting

Need help? Contact [Rookout support][2].

[1]: https://rookout.com
[2]: mailto:support@rookout.com
