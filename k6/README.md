# k6 Integration

## Overview

Track performance metrics of [k6][1] tests to:
- Correlate application performance with load testing metrics.
- Create alerts based on performance testing metrics.
- Analysis and visualize k6 metrics using the k6 Datadog Dashboard or [Metrics Explorer][5].

![k6 Datadog Dashboard][9]

## Setup

For the detailed instructions, follow the [k6 documentation][2]

### Step 1 - Copy your Datadog API Key

In Datadog, navigate to [Integrations --> API][3] and copy your API Key.

### Step 2 - Run the Datadog Agent

To get k6 metrics into Datadog, k6 has to send metrics to the Datadog Agent that will collect, aggregate, and forward the metrics to the Datadog platform.

You can run the Datadog Agent service as a Docker container with this command:

```shell
DOCKER_CONTENT_TRUST=1 \
docker run -d \
    --name datadog \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /proc/:/host/proc/:ro \
    -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
    -e DD_SITE="datadoghq.com" \
    -e DD_API_KEY=<YOUR_DATADOG_API_KEY> \
    -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=1 \
    -p 8125:8125/udp \
    datadog/agent:latest
```

Note that you have to replace `<YOUR_DATADOG_API_KEY>` with your API key, and if your account is registered with Datadog EU, the value of `DD_SITE` should be `datadoghq.eu`.

### Step 3 - Run the k6 test and output the results to Datadog

Once the Datadog Agent service is running, you can run the k6 test and send the metrics to the agent with:

```shell
k6 run --out datadog script.js
```

### Step 4 - Visualize the k6 metrics in Datadog

While running the test, k6 send metrics periodically to DataDog. By default, these metrics have `k6.` as name prefix. 

You can visualize k6 metrics in realtime at the [Datadog Metrics Explorer][5], creating [monitors][6] or [custom dashboards][7] for your performance testing metrics.

![k6 Datadog Metrics Explorer][8]

## Data Collected

### Metrics

See [metadata.csv][4] for a list of metrics provided by this integration.

### Service Checks

k6 does not include any service checks.

### Events

k6 does not include any events.

## Troubleshooting

Need help? Read the [k6 Datadog documentation](2) or contact the [k6 support][10].

[1]: https://k6.io/open-source
[2]: https://k6.io/docs/getting-started/results-output/datadog 
[3]: https://app.datadoghq.com/account/settings#api
[4]: https://github.com/k6io/integrations-extras/blob/master/k6/metadata.csv
[5]: https://docs.datadoghq.com/metrics/explorer/
[6]: https://docs.datadoghq.com/monitors/
[7]: https://docs.datadoghq.com/graphing/dashboards/
[8]: https://github.com/k6io/integrations-extras/blob/master/k6/images/metrics-explorer.png
[9]: https://github.com/k6io/integrations-extras/blob/master/k6/images/k6-datadog-dashboard.png
[10]: https://community.k6.io/

