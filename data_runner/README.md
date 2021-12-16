# Twenty Forty Eight

## Overview

The data runner is trapped in an infinite library, searching for your metrics. Open up a portal to watch him and see if you can get a better score than your peers! An idle game for the Datadog dashboard.

### What it does

Add the Data Runner widget to your dashboard, then choose a metric you want him to find. He'll run around the infinite library looking for it, and every time he finds it the metric's value will be added to your score. Leave him to run and see what your score is at the end of the day!

_Hang on, it can be any metric I feed into Datadog? So why wouldn't I just pick something with ridiculously high values?_

Why wouldn't you do that? I think `system.mem.committed_as` is some pretty big numbers; it's nice to have a game with a score of 1.4×10¹¹.

_Or even make up my own fictional metric and use the [Metrics Submission API](https://docs.datadoghq.com/api/latest/metrics/#submit-metrics) to send in really big numbers?_

See, _now_ you're gettin' it. Go wild.

### How it works, or: the techie bit

This is a [Datadog App](https://github.com/DataDog/apps) that provides a dashboard widget. It uses the standalone version of the [UI Extensions SDK](https://www.npmjs.com/package/@datadog/ui-extensions-sdk) ([ui-extensions-sdk.min.js](https://github.com/stuartlangridge/data-runner/blob/main/ui-extensions-sdk.min.js) in this repo, built from [the upstream github repo](https://github.com/DataDog/ui-extensions-sdk)). For a simpler sort of widget which does less work (and so may show off the required file structures more clearly) it may be useful to examine [dd-app-plain-html-grafana](https://github.com/stuartlangridge/dd-app-plain-html-grafana) or Datadog's own [starter kit](https://github.com/DataDog/starter-kit) for a React app.

On startup, it uses the [widget API client](https://github.com/DataDog/apps/blob/master/docs/en/programming-model.md#api-access) to query the [public Datadog API](https://docs.datadoghq.com/api/) to get a list of your metrics (which it can do because it has the `metrics_read` scope), and then dynamically updates its [widget settings menu](https://github.com/DataDog/apps/blob/master/docs/en/programming-model.md#widget-settings-menu) to list the metrics.

When you choose a metric (either on first adding the widget to your dashboard, or at any time later with the edit button), the Datadog dashboard fires a [`dashboard_custom_widget_options_change`](https://github.com/DataDog/apps/blob/master/docs/en/programming-model.md#widget-settings-menu) custom event which the runner code listens for and records the metric name.

Then periodically the runner polls the [metrics query API](https://docs.datadoghq.com/api/latest/metrics/#query-timeseries-points) for that chosen metric and takes the highest value since the last time it asked, and adds that to the runner's score.

The imagery is all from the fantastic [Kenney](https://kenney.nl/assets/isometric-library-tiles), and the font is from [ooqq](https://github.com/OOQQ/ZX-Spectrum-font).

## Setup

1. In your Datadog account, navigate to Dashboards. Select the dashboard that you would like to add the game to, or [create a new dashboard](https://docs.datadoghq.com/dashboards/#new-dashboard).

2. In the dashboard, click **+Add Widgets** to the right of the dashboard title. Scroll to the bottom to the "Apps" section, then drag and drop the **The data runner** widget into the desired position on your dashboard. Choose a metric you want the Data Runner to find, then click save.

## Support

[Contact Datadog support](https://www.datadoghq.com/support/) if you run in to any issues.

[Check out our app documentation](https://docs.datadoghq.com/developers/datadog_apps) if you are interested in building a Datadog app of your own.
