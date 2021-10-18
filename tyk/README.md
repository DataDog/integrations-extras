# Agent Check: Tyk

## Overview

![tyk logo][3]

![Illustration of Tyk in a lab][5]

Datadog can collect and display errors response time, duration, latency and monitor performance of the API traffic in [Tyk][1] to easily discover issues in your APIs or your consumers.

Tyk has a built-in Datadog integration that collects metrics from [Tyk API gateway][7].

Tyk API gateway records all the traffic that it's processing. It sends that information to Datadog and builds dashboards around it.

### How it works

[Tyk pump][23] writes custom application metrics and sends them into Datadog by sending them to [DogStatsD][9], a metrics aggregation service bundled with the Datadog Agent. DogStatsD implements the StatsD protocol which adds a few Datadog-specific extensions including the Histogram metric type, that is in use by `Tyk-gateway`.

`Tyk-gateway` uses `Tyk-pump` to send the analytics it generated to Datadog.

When running the Datadog Agent, DogstatsD gets the `request_time` metric from `Tyk-pump` in real time, per request, so you can understand the usage of your APIs and get the flexibility of aggregating by various parameters such as date, version, returned code, method etc.

The custom metric Tyk is using is of type [DD_HISTOGRAM_AGGREGATES][12].

## Setup

Tyk's integration is included in the `tyk-pump` package, so you only need to set configuration in the `pump.conf` (and there's no need to install anything on your Tyk platform).

### Installation

#### Install Tyk

For this integration you need to have a running Tyk installation. You can install [Tyk self managed][14] or [Tyk OSS][15]. Both options include the `tyk-pump`.

#### Install Datadog Agent

Install the [Datadog Agent][16] in your environment.

You can run Datadog [Agent][17] in your k8s cluster, as a docker container, on your mac, or any other way you choose as long as `Tyk pump` is be able to access it.

For containerized environments, see the [Autodiscovery Integration Templates][2] for more guidance. To validate that the changes are applied, [run the Agent's status subcommands][13]


### Configuration

#### Setup Tyk-pump:
To set a Datadog pump follow the instructions in [the DogstatsD section][18] of the pump README.

The following is an example of Datadog pump configuration in `pump.conf`:

``` json
pump.conf:
...
   "dogstatsd": {
      "type": "dogstatsd",
      "meta": {
        "address": "dd-agent:8126",
        "namespace": "tyk",
        "async_uds": true,
        "async_uds_write_timeout_seconds": 2,
        "buffered": true,
        "buffered_max_messages": 32,
        "sample_rate": 0.9999999999,
        "tags": [
          "method",
          "response_code",
          "api_version",
          "api_name",
          "api_id",
          "org_id",
          "tracked",
          "path",
          "oauth_id"
        ]
      }
    },
```

This [example][19] was taken from [Tyk-demo][20] project, an open source project that spins up a full tyk platform in one command and offers ready-made examples, including the Datadog example. To run this integration, use `up.sh analytics-datadog`.

#### Setup Datadog Agent

Tyk's integration uses [DogstatsD][21]. It is a metrics aggregation service bundled with the Datadog Agent. DogStatsD implements the `StatsD` protocol and adds a few Datadog-specific extensions. Tyk is using `Histogram metric type`.

Please set up the following Datadog and DogStatsD environment variables in your environment:

| DD Environment variable | Value | Description |
|---------------------------|-------------|------|
| DD_API_KEY | {your-datadog-api-key} | For the Datadog Agent to connect the DD portal. Your API key can be found in [Account Settings][22]. |
| DD_ENV |    tyk-demo-env   |   Sets the environment name. |
| DD_DOGSTATSD_TAGS | "env:tyk-demo" |  Additional tags to append to all metrics, events, and service checks received by this DogStatsD server. |
| DD_LOGS_ENABLED | true | Enables log collection for the Datadog Agent. |
| DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL | true | Collects logs from containers. |
| DD_DOGSTATSD_SOCKET | /var/run/docker.sock | Path to the Unix socket to listen to.  Docker compose mounts this path. |
| DD_DOGSTATSD_ORIGIN_DETECTION | true | Enables container detection and tagging for Unix socket metrics. |
| DD_DOGSTATSD_NON_LOCAL_TRAFFIC | true | Listens for DogStatsD packets from other containers. (Required to send custom metrics). |
| DD_AGENT_HOST | dd-agent | Name of the agent host in Docker. |
| DD_AC_EXCLUDE | redis | Excludes Datadog redis checks. (Optional) |
| DD_CONTAINER_EXCLUDE | true | Excludes docker checks for the Datadog Agent. |

After setting environment variables listed above, set up the agent [with DogstatsD][24].

[Restart the Agent][4] after setup.

### Validation

Create a dashboard or import [the sample][11] and add a widget. In the section **Graph your data** under the **metric** option, start typing the namespace you chose for the pump in the config `pump.conf` under `dogstatsd.namespace`.

In the example above it was `tyk`. Once you start typing you will see all the available metrics - `tyk.request_time.avg` etc.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Dashboards

With Datadog, you can create dashboards that display statistics about your API services and their consumption.

Here's an example for such a dashboard:

![Tyk Analytics dashboard example][10]

**Note: You can [import][11] the above dashboard and use it as an example or baseline for your own dashboard.**

### Events

The tyk integration does not include any events.

### Service Checks

The tyk integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][8].

[1]: https://tyk.io/
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/tyk/images/tyk_logo_no_bg.png
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/tyk/images/tyk-in-lab.png
[6]: https://github.com/DataDog/integrations-extras/blob/master/tyk/metadata.csv
[7]: https://github.com/TykTechnologies/tyk
[8]: https://docs.datadoghq.com/help/
[9]: https://docs.datadoghq.com/developers/dogstatsd/?tab=hostagent#pagetitle
[10]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/tyk/images/datadog-tyk-analytics-dashboard.jpg
[11]: https://github.com/DataDog/integrations-extras/blob/master/tyk/assets/dashboards/tyk_analytics_canvas.json
[12]: https://docs.datadoghq.com/agent/docker/?tab=standard#dogstatsd-custom-metrics
[13]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#agent-status-and-information
[14]: https://tyk.io/docs/tyk-self-managed/install/
[15]: https://tyk.io/docs/apim/open-source/installation/
[16]: https://app.datadoghq.com/account/settings#agent
[17]: https://docs.datadoghq.com/agent/
[18]: https://github.com/TykTechnologies/tyk-pump#dogstatsd
[19]: https://github.com/TykTechnologies/tyk-demo/blob/master/deployments/analytics-datadog/volumes/tyk-pump/pump-datadog.conf
[20]: https://github.com/TykTechnologies/tyk-demo/tree/master/deployments/analytics-datadog
[21]: https://docs.datadoghq.com/developers/dogstatsd/?tab=hostagent#setup
[22]: https://app.datadoghq.com/account/settings#api
[23]: https://tyk.io/docs/tyk-pump/
[24]: https://docs.datadoghq.com/developers/dogstatsd/?tab=hostagent#how-it-works