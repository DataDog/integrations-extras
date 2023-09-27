# Agent Check: Wayfinder

## Overview

[Wayfinder][1] is an infrastructure management platform that enables developer
self-service through a centralized configuration. This check monitors Wayfinder
key management components through the Datadog Agent.

The integration collects key metrics from the Wayfinder API server, controller,
and webhook components. These metrics should highlight issues in managed
workspaces. 

## Setup

Follow the instructions below to install the integration in the Wayfinder
Kubernetes management cluster.

### Installation

For containerized environments, the best way to use this integration with the
Docker Agent is to build the Agent with the Wayfinder integration installed. 

### Prerequisites:

A network policy must be configured to allow the Datadog Agent to connect to
Wayfinder components. The network policy below assumes Datadog is deployed to
the Datadog namespace and Wayfinder is deployed to the Wayfinder namespace.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: datadog-agent
  namespace: wayfinder
spec:
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: datadog
      podSelector:
        matchLabels:
          app: datadog-agent
    ports:
    - port: 9090
      protocol: TCP
  podSelector:
    matchExpressions:
    - key: name
      operator: In
      values:
      - wayfinder-controllers
      - wayfinder-apiserver
      - wayfinder-webhooks
  policyTypes:
  - Ingress
```

To build an updated version of the Agent:

1. Use the following Dockerfile:

    ```dockerfile
    FROM gcr.io/datadoghq/agent:latest

    ARG INTEGRATION_VERSION=1.0.0

    RUN agent integration install -r -t datadog-wayfinder==${INTEGRATION_VERSION}
    ```

2. Build the image and push it to your private Docker registry.

3. Upgrade the Datadog Agent container image. If you are using a Helm chart,
   modify the `agents.image` section in the `values.yaml` file to replace the
   default agent image:

    ```yaml
    agents:
      enabled: true
      image:
        tag: <NEW_TAG>
        repository: <YOUR_PRIVATE_REPOSITORY>/<AGENT_NAME>
    ```

4. Use the new `values.yaml` file to upgrade the Agent:

    ```shell
    helm upgrade -f values.yaml <RELEASE_NAME> datadog/datadog
    ```

### Configuration

1. Edit the `wayfinder/conf.yaml` file, in the `conf.d/` folder at the root of
   your Agent's configuration directory to start collecting your Wayfinder data.
   See the [sample wayfinder/conf.yaml][4] for all available configuration
   options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `wayfinder` under the Checks
section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Service Checks

Wayfinder does not include any service checks.

### Events

Wayfinder does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://www.appvia.io/product/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]:
    https://github.com/DataDog/integrations-extras/blob/master/wayfinder/datadog_checks/wayfinder/data/conf.yaml.example
[5]:
    https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]:
    https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]:
    https://github.com/DataDog/integrations-extras/blob/master/wayfinder/metadata.csv
[8]:
    https://github.com/DataDog/integrations-extras/blob/master/wayfinder/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/

