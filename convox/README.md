## Overview

Get metrics from Convox in real-time to visualize your containers' performance:

![snapshot](https://raw.githubusercontent.com/DataDog/integrations-extras/master/convox/images/snapshot.png)

## Setup

Please refer to the [Convox setup doc page](https://convox.com/docs/datadog/).

### Deploy the Datadog Agent

You can deploy the Datadog Agent as a Convox app with a very simple `docker-compose.yml` manifest:

```
# check out the repo
$ git clone https://github.com/convox-examples/dd-agent.git
$ cd dd-agent

# deploy the agent app and secret
$ convox apps create
$ convox env set API_KEY=<your api key>
$ convox deploy
$ convox scale agent --count=3 --cpu=10 --memory=128
```

Use a `count` that matches the `InstanceCount` parameter of your Rack.

### Auto Scaling

If autoscaling is enabled on your Rack, you’ll need to dynamically scale the Datadog agent count to match the Rack instance count.

See the [Listening for ECS CloudWatch Events Tutorial](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwet.html) for guidance.

## Data Collected
### Metrics
The Convox check does not include any metrics at this time.

### Events
The Convox check does not include any events at this time.

### Service Checks
The Convox check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).
