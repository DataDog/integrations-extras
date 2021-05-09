# JFrog Metrics Integration

## Overview
The following describes how to configure Datadog to gather metrics from JFrog Artifactory and JFrog Xray.

### What is JFrog Artifactory and Xray
JFrog Enterprise with Xray features Artifactory Enterprise and Xray. Together, they empower DevOps teams to improve their productivity to increase velocity and deliver high quality software releases with confidence. 

Artifactory supports multiple build packages, artifacts, and metadata. It allows DevOps teams to have the freedom of choice of build packages like Bower, Chef, CocoaPods, Conan, Conda, CRAN, Debian, Docker, Golang, Gradle, Git LFS, Helm, Ivy, Maven, npm, NuGet, Opkg, P2, PHP Composer, Puppet, PyPI, RPM, RubyGems, SBT, Vagrant & VCS, CI/CD platforms, and devops tools.

Artifactory Enterprise supports multi-region, multi-cloud, and hybrid replication for geographically distributed teams allowing you to replicate between a source repository and multiple targets simultaneously and security features such as IP filtering, CNAME, and data encryption at rest. Artifactory supports Kubernetes for microservices and containerized applications. Manage your deployments and gain insight into dependencies using Artifactory as your Kubernetes registry. 

JFrog Xray is a continuous security and universal artifact analysis solution that provides multi-layered analysis of your containers and software artifacts for vulnerabilities and license compliance issues.  It is the only Software Composition Analysis solution that natively integrates with JFrog Artifactory for optimized scanning and unified operation. Supports all major package types, understands how to unpack them, and uses recursive scanning to see into all of the underlying layers and dependencies, even those packaged in Docker images, and zip files.

### JFrog Artifactory Metrics API Dashboard

JFrog Artifactory’s Metrics API integration with Datadog allows you to send metrics from the Artifactory’s Open Metrics API endpoint to Datadog.  With this integration, you can gain insights into the system performance, storage consumption, and connection statistics associated with JFrog Artifactory.  Upon setting up the configuration, these metrics are made available as out-of-the-box dashboards within the Datadog UI and may be used to enhance existing dashboards within Datadog.

![artifactory][11]

### JFrog Xray Metrics API Dashboard

JFrog Xray Metrics API integration with Datadog allows you to send metrics from the Xray Metrics API to Datadog.  With this integration, you can gain insights into JFrog Xray’s system performance, as well as, insights into the count and type of artifacts and components scanned by Xray.  Upon setting up the configuration, these metrics are made available as out-of-the-box dashboards within the Datadog UI and may be used to enhance existing dashboards within Datadog.

![xray][12]

## Setup

### Installation

JFrog Metrics Integration uses OpenMetrics check which is included in the [Datadog Agent][1] package. So, a separate installation is not required.

### Artifactory and Xray Setup

1. [Enable Metrics for Artifactory][2]
2. [Create admin access tokens for Artifactory and Xray][3]

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

1. Edit the openmetrics.d/conf.yaml file at the root of your [Agent's configuration directory][4] to start collecting your Artifactory and Xray Metrics. See the [sample openmetrics.d/conf.yaml][5] for all available configuration options
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
          - jfxr*
    ```
2. [Restart the Agent][6]

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
[5]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_metrics/datadog_checks/jfrog_metrics/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#restart-the-agent
[7]: https://docs.datadoghq.com/agent/kubernetes/integrations/?tab=kubernetes
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[9]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_metrics/metadata.csv
[10]: https://docs.datadoghq.com/help/
[11]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_metrics/images/Artifactory_dashboard.png
[12]:  https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_metrics/images/xray_dashboard.png
