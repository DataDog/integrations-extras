# Apache APISIX Integration

## Overview

Apache APISIX is a dynamic, real-time, high-performance API gateway, and it provides rich traffic management features such as load balancing, dynamic upstream, canary release, circuit breaking, authentication, observability, and more. We could use Apache APISIX to handle traditional north-south traffic, as well as east-west traffic between services. It can also be used as a k8s ingress controller.

The [APISIX-Datadog plugin][1] pushes its custom metrics to the DogStatsD server, comes bundled with Datadog agent over the UDP connection. DogStatsD basically is an implementation of StatsD protocol. It collects the custom metrics for [Apache APISIX][2] agent, aggregates it into a single data point and sends it to the configured Datadog server.

## Setup

### Installation

Follow the Configuration instructions below.

### Configuration

1. If you are already using Datadog inside your infrastructure, you must have a datadog agent installed in your systems. It may either be a docker container, pod or binary for a respective package manager. In this case, you are good to go. Just make sure port 8125/udp is allowed through the firewall (if any) i.e more specifically, the Apache APISIX agent can reach port 8125 of the datadog agent. You may skip this subsection.

> To learn more about how to install a full-fledged datadog agent, visit [here][3].

2. If you are new to Datadog

   1. First create an account by visiting www.datadoghq.com.
   2. Generate an API Key.
      ![Generate an API Key](images/screenshot_1.png)

3. APISIX-Datadog plugin requires only the dogstatsd component of `datadog/agent` as the plugin asynchronously send metrics to the dogstatsd server following the statsd protocol over standard UDP socket. That's why APISIX recommends using the standalone `datadog/dogstatsd` image instead of using the full agent. It's extremely lightweight (only ~11 MB in size) compared to ~2.8GB of `datadog/agent` image.

To run it as a container:

```shell
# pull the latest image
$ docker pull datadog/dogstatsd:latest
# run a detached container
$ docker run -d --name dogstatsd-agent -e DD_API_KEY=<Your API Key from step 2> -p 8125:8125/udp  datadog/dogstatsd
```

If you are using Kubernetes in your production environment, you can deploy `dogstatsd` as a `Daemonset` or as a `Multi-Container Pod` alongside Apache APISIX agent.

4. The following is an example on how to activate the datadog plugin for a specific route. We are assuming your `dogstatsd` agent is already up an running.

```shell
# enable plugin for a specific route
$ curl http://127.0.0.1:9080/apisix/admin/routes/1 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d '
{
  "plugins": {
    "datadog": {}
  },
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "127.0.0.1:1980": 1
    }
  },
  "uri": "/hello"
}'
```

Now any requests to endpoint uri `/hello` will generate the above metrics and push it to local DogStatsD server of the datadog agent.

5. If we want to deactivate the plugin, simply remove the corresponding json configuration in the plugin configuration to disable the `datadog`. APISIX plugins are hot-reloaded, therefore no need to restart APISIX.

```shell
# disable plugin for a route
curl http://127.0.0.1:9080/apisix/admin/routes/1 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d '
{
  "uri": "/hello",
  "plugins": {},
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "127.0.0.1:1980": 1
    }
  }
}'
```

5. Please visit [Datadog Plugin][1]'s document for more custom configuration.

### Validation

Please [run the Agent's status subcommand][4] and look for `apisix` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this integration.

### Events

Apache APISIX check doesn't include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

## Further Reading

- [Cloud Monitoring with Datadog in Apache APISIX][7]

[1]: https://apisix.apache.org/docs/apisix/plugins/datadog
[2]: https://apisix.apache.org/
[3]: https://docs.datadoghq.com/agent/
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-core/blob/master/apache-apisix/metadata.csv
[6]: https://docs.datadoghq.com/help/
[7]: https://apisix.apache.org/blog/2021/11/12/apisix-datadog
