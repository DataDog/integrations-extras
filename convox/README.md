# Convox Integration

## Overview

Get metrics from Convox in real time to visualize your containers' performance.

![Convox integration dashboard widget][1]

## Setup

See the [Convox documentation][2] to set up the Datadog integration.

### Deploy the Datadog Agent

You can deploy the Datadog Agent as a Convox app by using a `docker-compose.yml` manifest. Use a `count` that matches the `InstanceCount` parameter of your Rack.

```shell
# check out the repo
$ git clone https://github.com/convox-examples/datadog.git
$ cd dd-agent

# deploy the agent app and secret
$ convox apps create
$ convox env set DD_API_KEY=<your api key>
$ convox deploy
$ convox scale agent --count=3 --cpu=10 --memory=128
```

Run `convox deploy` to deploy Datadog Agent into ECS.

### Auto scaling

If autoscaling is enabled on your Rack, you need to dynamically scale the Datadog Agent count to match the Rack instance count.

For more information, see the [Listening for ECS CloudWatch Events][3] tutorial.

## Data Collected

### Metrics

The Convox integration does not include any metrics.

### Events

The Convox integration does not include any events.

### Service Checks

The Convox integration does not include any service checks.

## Troubleshooting

When configuring environment variables in the `convox.yml` file, the `environment` parameter must be defined on the same level as the `services` parameter.

![The Environment and Services parameters defined on the same level][5]

Need help? Contact [Datadog support][4].

{{< partial name="whats-next/whats-next.html" >}}

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/convox/images/snapshot.png
[2]: https://docs.convox.com/integrations/monitoring/datadog
[3]: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwet.html
[4]: https://docs.datadoghq.com/help/
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/convox/images/setting_environment_variables.png
[6]: https://www.datadoghq.com/blog/monitor-aws-ecs-convox-integration/