# JFrog Metrics Integration

## Overview

This integration makes it easy for customers to monitor the health and operation of the JFrog platform and its related services.  Adopting the Metrics API enables JFrog to provide a richer dataset on Artifactory and Xray and make it easily consumable via predefined dashboards

## Setup

### Installation

JFrog Metrics Integration uses OpenMetrics check which is included in the [Datadog Agent] [1] package. So, a separate installation is not required

### Artifactory and Xray Setup

1. [Enable Metrics for Artifactory] [2]
2. [Create admin access tokens for Artifactory and Xray] [3]

### Datadog Configuration

Follow the instructions below to configure this check for an Agent running on a host. For containerized environments, see the Containerized section.

These values override the configuration specified below
```text
ARTIFACTORY_HOST_NAME_OR_IP   -> IP address or DNS of Artifactory 
ARTIFACTORY_ADMIN_TOKEN       -> Admin token for Artifactory
XRAY_ADMIN_TOKEN              -> Admin token for Xray
```
### Host
To configure this check for an Agent running on a host:

1. Edit the openmetrics.d/conf.yaml file at the root of your [Agent's configuration directory] [4] to start collecting your Artifactory and Xray Metrics. See the [sample openmetrics.d/conf.yaml][5] for all available configuration options
    ```text
    instances:
      - prometheus_url: http://<ARTIFACTORY_HOST_NAME_OR_IP>:80/artifactory/api/v1/metrics
        scheme: http
        headers:
          Authorization: "Bearer <ARTIFACTORY_ADMIN_TOKEN>"
        static_configs:
          - targets: ["<ARTIFACTORY_HOST_NAME_OR_IP>:80"]
        namespace: jfrog.artifactory
        metrics:
          - sys*
          - jfrt*
          - app*
      - prometheus_url: http://<ARTIFACTORY_HOST_NAME_OR_IP>:80/xray/api/v1/metrics
        scheme: http
        headers:
          Authorization: "Bearer <XRAY_ADMIN_TOKEN>"
        namespace: jfrog.xray
        metrics:
          - app*
          - db*
          - go*
          - queue*
          - sys*
    ```
2. [Restart the Agent] [6]

### Containerized
For containerized environments, see the [Autodiscovery Integration Templates][7] for guidance on applying the parameters specified above.

### Validation

[Run the Agent's status subcommand][8] and look for `openmetrics` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this check.

## Troubleshooting

Need help? Contact [Datadog support][10].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/jfrog/metrics#setup
[3]: https://www.jfrog.com/confluence/display/JFROG/Access+Tokens#AccessTokens-GeneratingAdminTokens
[4]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7#agent-configuration-directory
[5]: https://github.com/DataDog/integrations-core/blob/master/openmetrics/datadog_checks/openmetrics/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#restart-the-agent
[7]: https://docs.datadoghq.com/agent/kubernetes/integrations/?tab=kubernetes
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[9]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_metrics/metadata.csv
[10]: https://docs.datadoghq.com/help/