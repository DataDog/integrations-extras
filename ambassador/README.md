# Ambassador Integration

## Overview

Get metrics from [Ambassador][1] in real time to:

- Visualize the performance of your microservices

- Understand the impact of new versions of your services as you use Ambassador to do a canary rollout

![snapshot][2]

## Setup

Enable DogStatsD on your Agent Daemonset, and set the following environment variable on your Ambassador pod:

```
name: STATSD_HOST
valueFrom:
  fieldRef:    
    fieldPath: status.hostIP
```

With this setup, StatsD metrics are sent to the IP of the host, which redirects traffic to the Agent port 8125.

See [Envoy statistics with StatsD][5] for more information.

You can also send tracing data from Ambassador to Datadog APM. See [Distributed Tracing with Datadog][6] for more information.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this check.

### Events

The Ambassador check does not include any events.

### Service Checks

The Ambassador check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://www.getambassador.io
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ambassador/images/upstream-req-time.png
[3]: https://github.com/DataDog/integrations-extras/blob/master/ambassador/metadata.csv
[4]: https://docs.datadoghq.com/help/
[5]: https://www.getambassador.io/docs/edge-stack/latest/topics/running/statistics/envoy-statsd/
[6]: https://www.getambassador.io/docs/latest/howtos/tracing-datadog/
