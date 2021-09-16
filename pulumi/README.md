# Pulumi

## Overview

[Pulumi][1] is a modern infrastructure as code platform that enables cloud engineering teams to define, deploy and manage cloud resources on any cloud using their favorite programming languages.

The Pulumi integration is used to provision any of the cloud resources available in Datadog. This integration must be configured with credentials to deploy and update resources in Datadog.

## Setup

### Installation

The [Pulumi Datadog integration][2] uses the Datadog SDK to manage and provision resources.

### Configuration

1. [Sign up for a free or commercial Pulumi account][3]

2. [Install Pulumi][4]

3. Once obtained, there are two ways to set your Datadog authorization tokens for Pulumi:


Set the environment variables `DATADOG_API_KEY` and `DATADOG_APP_KEY`:

```
export DATADOG_API_KEY=XXXXXXXXXXXXXX && export DATADOG_APP_KEY=YYYYYYYYYYYYYY
```

Or, set them using configuration if you prefer that they be stored alongside your Pulumi stack for easier multi-user access:

```
pulumi config set datadog:apiKey XXXXXXXXXXXXXX --secret && pulumi config set datadog:appKey YYYYYYYYYYYYYY --secret
```

**Note**: Pass `--secret` when setting `datadog:apiKey` and `datadog:appKey` so that they are properly encrypted.

4. Run `pulumi new` to initialize a project directory for your infrastructure stack and follow the [API documentation][5] to define new metrics, monitors, dashboards, or other resources.

5. Once you have defined your cloud resources in code, run `pulumi up` to create the new resources defined in your Pulumi program. 

## Data Collected

### Metrics

Pulumi does not include any metrics.

### Service Checks

Pulumi does not include any service checks.

### Events

Pulumi does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://pulumi.com
[2]: https://www.pulumi.com/docs/intro/cloud-providers/datadog/
[3]: https://www.pulumi.com/pricing/
[4]: https://www.pulumi.com/docs/get-started/
[5]: https://www.pulumi.com/docs/reference/pkg/datadog/
[6]: https://docs.datadoghq.com/help/
