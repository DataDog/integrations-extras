# Agent Check: opa

## Overview

This check collects metrics from [Open Policy Agent][1].

## Setup

Follow the instructions below to install and configure this check for an Agent running on a Kubernetes cluster. See also the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the opa check on your Kubernetes cluster:

1. Install the [developer toolkit][3].
2. Clone the `integrations-extras` repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `opa` package, run:

   ```shell
   ddev -e release build opa
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
    kubectl exec ds/datadog -- agent integration install -w <PATH_OF_OPA_ARTIFACT_>/<OPA_ARTIFACT_NAME>.whl
    ```

11. Run the following commands to copy the checks and configuration to the corresponding PVCs:

    ```shell
    kubectl exec ds/datadog -- sh
    # cp -R /opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/* /checksd
    # cp -R /etc/datadog-agent/conf.d/* /confd
    ```

12. Restart the Datadog Agent pods.

### Logs-generated metrics

The default dashboard includes some graphs related to a metric around OPA decisions, called `opa.decisions`. This metric is created based on the OPA "Decision Logs". To generate this metric and populate this part of the dashboard, you will need to create a new log-generated metric in Datadog.

First, we will create a facet for the `msg` field of our OPA logs, as we will only generate metrics for the "Decision Logs" type of log entry. For that, select any of the log entries coming from OPA, click on the engine log near the `msg` field and select "Create facet for @msg":

![Message Facet][6]

Now we need to create two facets, one for the `input.request.kind.kind` field and one for the `result.response.allowed` field, both available in any of the log entries type "Decision Log".

![Kind Facet][7]
![Allowed Facet][8]

Once you have created the facets, we are ready to generate the needed metric for the Dashboard to be complete. Click on the menu "Logs -> Generate Metrics". Click on "Add a new metric" and fill the form with the following data:

![OPA Decision Metric][9]

### Configuration

1. Edit the `opa/conf.yaml` file, in the `/confd` folder that you added to the Agent pod to start collecting your opa performance data. See the [sample opa/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][10].

### Validation

[Run the Agent's status subcommand][11] and look for `opa` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this check.

### Service Checks

`opa.prometheus.health`:
Returns CRITICAL if the Agent fails to connect to the Prometheus endpoint, otherwise returns UP.

`opa.health`
Returns `CRITICAL` if the agent fails to connect to the OPA health endpoint, `OK` if it returns 200, `WARNING` otherwise.

`opa.bundles_health`
Returns `CRITICAL` if the agent fails to connect to the OPA bundles health endpoint, `OK` if it returns 200, `WARNING` otherwise.

`opa.plugins_health`
Returns `CRITICAL` if the agent fails to connect to the OPA plugins health endpoint, `OK` if it returns 200, `WARNING` otherwise.

### Events

opa does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][13].

[1]: https://www.openpolicyagent.org/
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://docs.datadoghq.com/agent/kubernetes/daemonset_setup/?tab=k8sfile
[5]: https://github.com/DataDog/integrations-extras/blob/master/opa/datadog_checks/opa/data/conf.yaml.example
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/opa/images/msg_facet.png
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/opa/images/kind_facet.png
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/opa/images/allowed_facet.png
[9]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/opa/images/metric.png
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[12]: https://github.com/DataDog/integrations-core/blob/master/opa/metadata.csv
[13]: https://docs.datadoghq.com/help/
