# Agent Check: gatekeeper 

## Overview

This check collects metrics from [OPA Gatekeeper][1].

## Setup

Follow the instructions below to install and configure this check for an Agent running on a Kubernetes cluster. See also the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the gatekeeper check on your Kubernetes cluster:

1. Install the [developer toolkit][3].
2. Clone the `integrations-extras` repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `gatekeeper` package, run:

   ```shell
   ddev -e release build gatekeeper
   ```

5. [Download the Agent manifest to install the Datadog Agent as a DaemonSet][4].
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
    kubectl exec ds/datadog -- agent integration install -w <PATH_OF_GATEKEEPER_ARTIFACT_>/<GATEKEEPER_ARTIFACT_NAME>.whl
    ```

11. Run the following commands to copy the checks and configuration to the corresponding PVCs:

    ```shell
    kubectl exec ds/datadog -- sh
    # cp -R /opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/* /checksd
    # cp -R /etc/datadog-agent/conf.d/* /confd
    ```

12. Restart the Datadog Agent pods.

### Configuration

1. Edit the `gatekeeper/conf.yaml` file, in the `/confd` folder that you added to the Agent pod to start collecting your gatekeeper performance data. See the [sample gatekeeper/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `gatekeeper` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

`gatekeeper.health`
Returns `CRITICAL` if the agent fails to connect to the gatekeeper health endpoint, `OK` if it returns 200, `WARNING` otherwise.

### Events

gatekeeper does not include any events.

## Troubleshooting

Need help? Contact [Datadog support[9].

[1]: https://github.com/open-policy-agent/gatekeeper
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://docs.datadoghq.com/agent/kubernetes/daemonset_setup/?tab=k8sfile
[5]: https://github.com/DataDog/integrations-extras/blob/master/gatekeeper/datadog_checks/gatekeeper/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-core/blob/master/gatekeeper/metadata.csv
[9]: https://docs.datadoghq.com/help/
