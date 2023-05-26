# Convox Integration

## Overview

You can add operational visibility to your Convox environments with Datadog for both v2 (ECS) and v3 (cloud agnostic Kubernetes) racks.

![Convox integration dashboard widget][1]

## Setup

See the Convox documentation for specific instructions to set up Datadog for your rack version:
[v2 Docs][2]
[v3 Docs][6]

### Deploy the Datadog Agent

You can deploy the Datadog Agent as a Convox app by using the provided agent example from our documentation for the `convox.yml` manifest and a basic `DOCKERFILE`.

## Troubleshooting

When configuring environment variables in the `convox.yml` file, it is important to ensure all levels of indentation match examples given in our configuration documention.

Please be sure your DataDog API Key is correctly set as an ENV variable or else the agent will fail to deploy.

Need help? Contact [Datadog support][4].

## Further Reading

Additional helpful documentation, links, and articles:

- [Monitor your AWS ECS platform with Convox and Datadog][5]

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/convox/images/snapshot.png
[2]: https://docs.convox.com/integrations/monitoring/datadog
[3]: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwet.html
[4]: https://docs.datadoghq.com/help/
[5]: https://www.datadoghq.com/blog/monitor-aws-ecs-convox-integration/
[6]: https://docsv2.convox.com/introduction/getting-started