# Rookout for Datadog

## Overview

### Description

[Rookout][1] is a disruptive developer solution for cloud native debugging and live data collection. Rookout’s Non-Breaking Breakpoints let you collect any type of data on the fly with no extra coding, redeployments, or restarts.

Rookout is designed from the ground up for production environments and modern architecture debugging, such as Kubernetes, microservices, serverless, and service-mesh based applications.

The Rookout integration lets you quickly collect metrics from your code running live in production or any other environment, without ever needing to stop it or to redeploy.

### Usage

The Rookout integration has two components: the first is a context menu item for your dashboard widgets that lets you quickly start collecting metric points from your code, and the second is a custom widget showing you all the metric points you have set in Rookout.

**Context Menu Item**

When clicking on a timeseries widget that represents one or more servers or services, a new context menu item will appear. 

Clicking on "Set metric points" will open the Rookout app, and automatically select the right instances for you.

**Custom Dashboard Widget**

Add the Rookout Widget to your dashboard to see where you have set metric points.

## Setup

### Configuration

To add the Rookout context menu item to a timeseries widget in your dashboard, you need to add a rookout label filter to its title.

For instance, if a timeseries shows some metric in a service called "cartservice", you would want the Rookout context menu item to automatically start a Rookout session with the label filter: "k8s_deployment:cartservice".

To do that, add "\[k8s_deployment:cartservice\]" to the title of the timeseries widget.

## Data Collected

### Metrics

Rookout does not include any metrics.

### Service Checks

Rookout does not include any service checks.

### Events

Rookout does not include any events.

## Troubleshooting

Feel free to contact us at [support@rookout.com][2]

[1]: https://rookout.com
[2]: mailto:support@rookout.com
