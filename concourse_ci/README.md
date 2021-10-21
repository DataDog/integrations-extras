# Concourse CI Integration

## Overview

Configure the Datadog Metric Emitter in Concourse CI to:

- Visualize the duration of pipelines, number of containers and mounted volumes of workers.
- Identify slow requests to build routes.

## Setup

### Installation

Concourse CI comes bundled with a Datadog metrics emitter. A prerequisite to configuring [ATC][1] to emit metrics on start is to have a [Datadog Agent][2] installed.

### Configuration

Configure ATC to use the Datadog emitter by setting the following options. It is important to use a prefix of `concourse.ci` to avoid emitting [custom metrics][3].

### Metric emitter options

See the Concourse CI [documentation][4] for more information.

```text
Metric Emitter (Datadog):
    --datadog-agent-host=       Datadog agent host to expose dogstatsd metrics [$CONCOURSE_DATADOG_AGENT_HOST]
    --datadog-agent-port=       Datadog agent port to expose dogstatsd metrics [$CONCOURSE_DATADOG_AGENT_PORT]
    --datadog-prefix=           Prefix for all metrics to easily find them in Datadog [$CONCOURSE_DATADOG_PREFIX]
```

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.

### Events

This integration does not support events.

### Service

This integration does not collect service checks.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://concourse-ci.org/concepts.html
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/developers/metrics/custom_metrics/
[4]: https://concourse-ci.org/metrics.html#configuring-metrics
[5]: https://github.com/DataDog/integrations-extras/blob/master/concourse_ci/metadata.csv
[6]: https://docs.datadoghq.com/help/
