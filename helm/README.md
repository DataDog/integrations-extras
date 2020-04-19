# Agent Check: helm

## Overview

This check monitors [helm][1] through the Datadog Agent.

It mirrors the output values of [helm-exporter][8].  You should expect a metric value of -1
if the helm chart fails to install.  Here is the complete status map:

```py
STATUS_MAP = {
    "unknown": 0,
    "deployed": 1,
    "uninstalled": 2,
    "superseded": 3,
    "failed": -1,
    "uninstalling": 5,
    "pending-install": 6,
    "pending-upgrade": 7,
    "pending-rollback": 8,
}
```

Because helm uses k8s secrets to store metadata, you'll also need to give the
pod running the helm check permissions to list secrets.  That will involve
* A cluster-role that can list secrets
* A role binding between the cluster role and your pod's service account

It may look like the following:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: a-name-for-your-role
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - list
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: a-name-for-your-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: a-name-for-your-role
subjects:
- kind: ServiceAccount
  name: datadog
  namespace: datadog
```


## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.  It also assumes your pod has the correct permissions to list secrets.

### Installation

To install the helm check on your host:

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit) on any machine.
2. Run `ddev release build helm` to build the package.
3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).
4. Upload the build artifact to any host with an Agent andrun `datadog-agent integration install -w path/to/helm/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `helm.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your helm performance data. See the [sample helm.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `helm` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

helm does not include any service checks.

### Events

helm does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://helm.sh/
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://github.com/DataDog/integrations-core/blob/master/helm/datadog_checks/helm/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-core/blob/master/helm/metadata.csv
[7]: https://docs.datadoghq.com/help
[8]: https://github.com/sstarcher/helm-exporter
