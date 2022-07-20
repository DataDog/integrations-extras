# Agent Check: cert_manager

## Overview

This check collects metrics from [cert-manager][1].

![Cert-Manager Overview Dashboard][2]

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

#### Agent versions >=7.26.0 or >=6.26.0

To use an integration from `integrations-extra` with the Docker Agent, Datadog recommends building the Agent with the integration installed. Use the following Dockerfile to build an updated version of the Agent that includes the `cert_manager` integration from `integrations-extras`:

```
FROM gcr.io/datadoghq/agent:latest
RUN agent integration install -r -t datadog-cert_manager==<INTEGRATION_VERSION>
```

#### Agent versions <7.26.0 or <6.26.0

To install the cert_manager check on your host:

1. Install the [developer toolkit][4].
2. Clone the `integrations-extras` repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `cert_manager` package, run:

   ```shell
   ddev -e release build cert_manager
   ```

5. [Download the Agent manifest to install the Datadog Agent as a DaemonSet][5].
6. Create two `PersistentVolumeClaim`s, one for the checks code, and one for the configuration.
7. Add them as volumes to your Agent pod template and use them for your checks and configuration:

   ```yaml
        env:
          - name: DD_CONFD_PATH
            value: "/confd"
          - name: DD_ADDITIONAL_CHECKSD
            value: "/checksd"
      [...]
        volumeMounts:
          - name: agent-code-storage
            mountPath: /checksd
          - name: agent-conf-storage
            mountPath: /confd
      [...]
      volumes:
        - name: agent-code-storage
          persistentVolumeClaim:
            claimName: agent-code-claim
        - name: agent-conf-storage
          persistentVolumeClaim:
            claimName: agent-conf-claim
   ```

8. Deploy the Datadog Agent in your Kubernetes cluster:

   ```shell
   kubectl apply -f agent.yaml
   ```

9. Copy the integration artifact .whl file to your Kubernetes nodes or upload it to a public URL

10. Run the following command to install the integrations wheel with the Agent:

    ```shell
    kubectl exec $(kubectl get pods -l app=datadog-agent -o jsonpath='{.items[0].metadata.name}') -- agent integration install -w <PATH_OF_CERT_MANAGER_ARTIFACT_>/<CERT_MANAGER_ARTIFACT_NAME>.whl
    ```

11. Run the following commands to copy the checks and configuration to the corresponding PVCs:

    ```shell
    kubectl exec $(kubectl get pods -l app=datadog-agent -o jsonpath='{.items[0].metadata.name}') -- cp -R /opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/* /checksd
    kubectl exec $(kubectl get pods -l app=datadog-agent -o jsonpath='{.items[0].metadata.name}') -- cp -R /etc/datadog-agent/conf.d/* /confd
    ```

12. Restart the Datadog Agent pods.

### Configuration

1. Edit the `cert_manager.d/conf.yaml` file, in the `/confd` folder that you added to the Agent pod to start collecting your cert_manager performance data. See the [sample cert_manager.d/conf.yaml][6] for all available configuration options.

2. [Restart the Agent][7].

### Validation

[Run the Agent's status subcommand][8] and look for `cert_manager` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this check.

### Events

cert_manager does not include any events.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][10].


[1]: https://github.com/jetstack/cert-manager
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/cert_manager/images/overview_dashboard.png
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[5]: https://docs.datadoghq.com/agent/kubernetes/daemonset_setup/?tab=k8sfile
[6]: https://github.com/DataDog/integrations-extras/blob/master/cert_manager/datadog_checks/cert_manager/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[9]: https://github.com/DataDog/integrations-extras/blob/master/cert_manager/metadata.csv
[10]: https://docs.datadoghq.com/help/
[11]: https://github.com/DataDog/integrations-extras/blob/master/cert_manager/assets/service_checks.json
