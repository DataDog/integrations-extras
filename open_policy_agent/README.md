# Agent Check: open_policy_agent 

## Overview

This check collects metrics from [Open Policy Agent][1].

## Setup

Follow the instructions below to install and configure this check for an Agent running on a Kubernetes cluster. See also the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the open_policy_agent check on your Kubernetes cluster:

1. Install the [developer toolkit][3].
2. Clone the `integrations-extras` repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `open_policy_agent` package, run:

   ```shell
   ddev -e release build open_policy_agent
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

9. Copy the integration artifact .whl file to your Kubernetes nodes or upload it to a public URL.

10. Run the following command to install the integrations wheel with the Agent:

    ```shell
    kubectl exec ds/datadog -- agent integration install -w <PATH_OF_OPEN_POLICY_AGENT_ARTIFACT_>/<OPEN_POLICY_AGENT_ARTIFACT_NAME>.whl
    ```

11. Run the following commands to copy the checks and configuration to the corresponding PVCs:

    ```shell
    kubectl exec ds/datadog -- sh
    # cp -R /opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/* /checksd
    # cp -R /etc/datadog-agent/conf.d/* /confd
    ```

12. Restart the Datadog Agent pods.

### Logs-generated metrics

The default dashboard includes some graphs related to a metric around OPA decisions, called `open_policy_agent.decisions`. This metric is created based on the OPA "Decision Logs". To generate this metric and populate this part of the dashboard, create a new log-generated metric in Datadog.

First, create a facet for the `msg` field of the OPA logs, as it only generates metrics for the "Decision Logs" type of log entry. For that, select any of the log entries coming from OPA, click on the engine log near the `msg` field and select "Create facet for @msg":

![Message Facet][6]

Create two facets, one for the `input.request.kind.kind` field and one for the `result.response.allowed` field, both available in any of the log entries type "Decision Log".

![Kind Facet][7]
![Allowed Facet][8]

Once you have created the facets, generate the needed metric for the Dashboard to be complete. Click on the menu "Logs -> Generate Metrics". Click on "Add a new metric" and fill in the form with the following data:

![OPA Decision Metric][9]

### Configuration

1. Edit the `open_policy_agent/conf.yaml` file, in the `/confd` folder that you added to the Agent pod to start collecting your OPA performance data. See the [sample open_policy_agent/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][10].

### Validation

[Run the Agent's status subcommand][11] and look for `open_policy_agent` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this check.

### Events

open_policy_agent does not include any events.

### Service Checks

See [service_checks.json][14] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][13].


[1]: https://www.openpolicyagent.org/
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://docs.datadoghq.com/agent/kubernetes/daemonset_setup/?tab=k8sfile
[5]: https://github.com/DataDog/integrations-extras/blob/master/open_policy_agent/datadog_checks/open_policy_agent/data/conf.yaml.example
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/open_policy_agent/images/msg_facet.png
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/open_policy_agent/images/kind_facet.png
[8]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/open_policy_agent/images/allowed_facet.png
[9]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/open_policy_agent/images/metric.png
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[12]: https://github.com/DataDog/integrations-core/blob/master/open_policy_agent/metadata.csv
[13]: https://docs.datadoghq.com/help/
[14]: https://github.com/DataDog/integrations-extras/blob/master/open_policy_agent/assets/service_checks.json
