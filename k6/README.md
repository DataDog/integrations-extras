# k6 Integration

## Overview

[k6][1] is an open-source load testing tool that will help you to catch performance issues and performance regressions earlier.

With the k6 integration, you can track performance metrics of k6 tests to:

- Correlate application performance with load testing metrics.
- Create alerts based on performance testing metrics.
- Analyze and visualize k6 metrics using the k6 Datadog Dashboard or [Metrics Explorer][5].

![k6 Datadog Dashboard][9]

## Setup

For the detailed instructions, follow the [k6 documentation][2].

### Installation

1. In Datadog, navigate to Integrations > [API][3] to copy your API key.


2. Run the Datadog Agent:

    To get k6 metrics into Datadog, k6 sends metrics through the Datadog Agent, which collects, aggregates, and forwards the metrics to the Datadog platform.

    Run the Datadog Agent service as a Docker container with this command:

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

    **Note**: Replace `<YOUR_DATADOG_API_KEY>` with your [API][3] key. If your account is registered with Datadog EU, change the value of `DD_SITE` to `datadoghq.eu`.

3. Run the k6 test and output the results to Datadog.

    Once the Datadog Agent service is running, run the k6 test and send the metrics to the Agent with:

    ```shell
    K6_STATSD_ENABLE_TAGS=true k6 run --out statsd script.js
    ```

4. Visualize the k6 metrics in Datadog.

    While running the test, k6 sends metrics periodically to DataDog. By default, these metrics have `k6.` as the name prefix. 

    You can visualize k6 metrics in realtime with the [metrics explorer][5], [monitors][6], or [custom dashboards][7].

    ![k6 Datadog Metrics Explorer][8]

    Additionally, the first time Datadog detects the `k6.http_reqs` metric, the k6 integration tile is installed automatically, and the default k6 dashboard is added to your [dashboard list][11].

    ![k6 Datadog Dashboard][9]


## Data Collected

### Metrics

See [metadata.csv][4] for a list of metrics provided by this integration.

### Service Checks

The k6 integration does not include any service checks.

### Events

The k6 integration does not include any events.

## Troubleshooting

Need help? Read the [k6 Datadog documentation][2] or contact [k6 support][10].

[1]: https://k6.io/open-source
[2]: https://k6.io/docs/results-visualization/datadog
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://github.com/DataDog/integrations-extras/blob/master/k6/metadata.csv
[5]: https://docs.datadoghq.com/metrics/explorer/
[6]: https://docs.datadoghq.com/monitors/
[7]: https://docs.datadoghq.com/graphing/dashboards/
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/k6/images/metrics-explorer.png
[9]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/k6/images/k6-default-dashboard.png
[10]: https://community.k6.io/
[11]: https://docs.datadoghq.com/dashboards/#dashboard-list
