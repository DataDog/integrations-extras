# Agent Check: cert_manager

## Overview

This check collects metrics from [cert-manager][1] .

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the cert_manager check on your host:

1. Install the [developer toolkit][3].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `cert_manager` package, run:

    ```
    ddev -e release build cert_manager
    ```

5. [Download the manifest to install the Datadog agent as a Daemonset][4].
6. Create two PersistentVolumeClaim, one for the checks code, one for the configuration.
7. Add them as volumes to your agent pod template and use them for your checks and configuration as:

   ```
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

8. Deploy the Datadog agent in your Kubernetes cluster:

   ```
   kubectl apply -f agent.yaml
   ```

9. Copy the integration artifact .whl file to your Kubernetes nodes or upload it to a public URL

10. Run the following command to install the integrations wheel with the Agent:

   ```
   kubectl exec $(kubectl get pods -l app=datadog-agent -o jsonpath='{.items[0].metadata.name}') -- agent integration install -w <PATH_OF_CERT_MANAGER_ARTIFACT_>/<CERT_MANAGER_ARTIFACT_NAME>.whl
   ```

11. Run the following commands to copy the checks and configuration to the corresponding PVCs:

```
kubectl exec $(kubectl get pods -l app=datadog-agent -o jsonpath='{.items[0].metadata.name}') -- cp -R /opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/* /checksd
kubectl exec $(kubectl get pods -l app=datadog-agent -o jsonpath='{.items[0].metadata.name}') -- cp -R /etc/datadog-agent/conf.d/* /confd
```

12. Restart the Datadog agent pods

### Configuration

1. Edit the `cert_manager.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your cert_manager performance data. See the [sample cert_manager.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `cert_manager` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

`cert_manager.prometheus.health`:
Returns CRITICAL if the Agent fails to connect to the prometheus endpoint, otherwise returns UP.

### Events

cert_manager does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://github.com/jetstack/cert-manager
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://docs.datadoghq.com/agent/kubernetes/daemonset_setup/?tab=k8sfile
[5]: https://github.com/DataDog/integrations-extras/blob/master/cert_manager/datadog_checks/cert_manager/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[8]: https://github.com/DataDog/integrations-core/blob/master/cert_manager/metadata.csv
[9]: https://docs.datadoghq.com/help
