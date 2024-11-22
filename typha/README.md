# Agent Check: Typha

## Overview

This check monitors [Typha][1] to collect Prometheus metrics through the Datadog Agent.

## Enabling Prometheus Metrics

To enable Prometheus metrics, configure the following variables in the `Typha` deployment:

```yaml
TYPHA_PROMETHEUSMETRICSENABLED: "true"
TYPHA_PROMETHEUSMETRICSPORT: "9093"
```

See the official [documentation][2] for more information.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a Kubernetes cluster. See also the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

To install the Typha check on your Kubernetes environment, use the following Dockerfile to build an updated version of the Agent that includes the `typha` integration from `integrations-extras`:

```
FROM gcr.io/datadoghq/agent:latest
RUN agent integration install -r -t datadog-typha==<INTEGRATION_VERSION>
```

You can also build the release and use the `.whl` package to install it:

1. Install the [developer toolkit][4].
2. Clone the `integrations-extras` repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `typha` package, run:

   ```shell
   ddev -e release build typha
   ```
5. Build your Docker image with the integration installed:

```
FROM gcr.io/datadoghq/agent:latest
COPY <WHEEL_PACKAGE_NAME> <DESTINATION>
RUN agent integration install -r -w <DESTINATION>/<WHEEL_PACKAGE_NAME> \
     && rm -rf <DESTINATION>/<WHEEL_PACKAGE_NAME>
```

### Configuration

1. Set `datadog.confd` definition for `typha` integration:

```yaml
  typha.yaml: |-
    ad_identifiers:
      - typha
    init_config:
    instances:
      - prometheus_url: http://%%host%%:9093/metrics
```

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][5] and look for `typha` under the Checks section.

For containerized environment:

```sh
kubectl exec -it <DATADOG_POD> -n <NAMESPACE> -- agent status
```

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration.

### Events

Typha does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://docs.tigera.io/calico/latest/reference/typha/
[2]: https://docs.tigera.io/calico/latest/reference/typha/configuration#general-configuration
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://docs.datadoghq.com/developers/integrations/python
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://github.com/DataDog/integrations-extras/blob/master/typha/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/typha/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
