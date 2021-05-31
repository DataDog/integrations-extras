

## Overview
The following describes how to configure Datadog to gather metrics from JFrog Artifactory and JFrog Xray.

### What is JFrog Artifactory and Xray
JFrog Enterprise with Xray features Artifactory Enterprise and Xray. Together, they empower DevOps teams to improve their productivity to increase velocity and deliver high quality software releases with confidence. 

Artifactory supports multiple build packages, artifacts, and metadata. It allows DevOps teams to have the freedom of choice of build packages like Bower, Chef, CocoaPods, Conan, Conda, CRAN, Debian, Docker, Golang, Gradle, Git LFS, Helm, Ivy, Maven, npm, NuGet, Opkg, P2, PHP Composer, Puppet, PyPI, RPM, RubyGems, SBT, Vagrant & VCS, CI/CD platforms, and devops tools.

Artifactory Enterprise supports multi-region, multi-cloud, and hybrid replication for geographically distributed teams allowing you to replicate between a source repository and multiple targets simultaneously and security features such as IP filtering, CNAME, and data encryption at rest.Artifactory supports Kubernetes for microservices and containerized applications. Manage your deployments and gain insight into dependencies using Artifactory as your Kubernetes registry. 

JFrog Xray is a continuous security and universal artifact analysis solution that provides multi-layered analysis of your containers and software artifacts for vulnerabilities and license compliance issues.  It is the only Software Composition Analysis solution that natively integrates with JFrog Artifactory for optimized scanning and unified operation. Supports all major package types, understands how to unpack them, and uses recursive scanning to see into all of the underlying layers and dependencies, even those packaged in Docker images, and zip files.

### JFrog Artifactory Datadog Dashboard

JFrog Datadog integration allows you to send Artifactory logs to the log stream in Datadog. You can use it to enhance your existing dashboards or to gain more insight into Artifactory's usage statistics.

![dashboard][1]

### JFrog Artifactory and Xray Metrics API Dashboard

JFrog Artifactory’s/Xray's Metrics API integration with Datadog allows you to send metrics from the Artifactory’s/Xray's Open Metrics API endpoint to Datadog.  With this integration, you can gain insights into the system performance, storage consumption, and connection statistics associated with JFrog Artifactory/Xray, as well as, insights into the count and type of artifacts and components scanned by Xray.  Upon setting up the configuration, these metrics are made available as out-of-the-box dashboards within the Datadog UI and may be used to enhance existing dashboards within Datadog.

![artifactory][2]

![xray][3]

## Setup

### Requirements

* Kubernetes Cluster
* JFrog Artifactory and/or JFrog Xray installed via [JFrog Helm Charts][4]
* [Helm 3][5]
* Your [Datadog API key][6].

### Logs Collection
1. Fluentd configuration : Datadog's Fluentd plugin can be used to forward logs directly from Fluentd to your Datadog account.

    Set up the Fluentd integration by specifying the API key as follows:

    _api_key_ is your [Datadog API key][6].

    _dd_source_ attribute is set to the name of the log integration in your logs in order to trigger the integration automatic setup in Datadog.

    _include_tag_key_ defaults to false and it will add fluentd tag in the JSON record if set to true

    Adding proper metadata is the key to unlocking the full potential of your logs in Datadog. By default, the hostname and timestamp fields should be remapped.

    ```
    <match jfrog.**>
    @type datadog
    @id datadog_agent_artifactory
    api_key <api_key>
    include_tag_key true
    dd_source fluentd
    </match>
    ```

2. Integration enablement

    To enable this integration, run the td-agent on `artifactory` pods:

    ``` 
    td-agent
    ```

    The API key is configured in `td-agent`, which will start sending logs to Datadog. 

    Add all attributes as facets from **Facets** > **Add** (on the left side of the screen in Logs) > **Search**.

### Metrics Collection

1. Enable Metrics for Artifactory and Xray

    1. [Enable Metrics for Artifactory][7]
    2. [Create admin access tokens for Artifactory and Xray][8]

2. Datadog Configuration

    Follow the instructions below to configure this check for an Agent running on a host. For containerized environments, see the Containerized section.

    These values override the configuration specified below
    ```text
    ARTIFACTORY_HOST_NAME_OR_IP   -> IP address or DNS of Artifactory 
    ARTIFACTORY_ADMIN_TOKEN       -> Admin token for Artifactory
    XRAY_ADMIN_TOKEN              -> Admin token for Xray
    ```
    #### Host
    To configure this check for an Agent running on a host:

    1. Edit the openmetrics.d/conf.yaml file at the root of your [Agent's configuration directory][9] to start collecting your Artifactory and Xray Metrics. See the [sample openmetrics.d/conf.yaml][10] for all available configuration options
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
    2. [Restart the Agent][11]

    #### Containerized
    For containerized environments, see the [Autodiscovery Integration Templates][12] for guidance on applying the parameters specified above.

    #### Validation

    [Run the Agent's status subcommand][13] and look for `openmetrics` under the Checks section.

### JFrog platform tile 

If you have not installed the JFrog platform tile yet, install the tile.

### JFrog Artifactory Dashboard

Go to Dashboard -> Dashboard List, find `JFrog Artifactory Dashboard`, `Atifactory Metrics`, `Xray Metrics` and explore it.

### Data Collected

#### Metrics

See [metadata.csv][14] for a list of metrics provided by this check.

## Troubleshooting

Need help? Contact [Datadog support][15].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/dashboard.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/artifactory_metrics_dashboard.png
[3]:  https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/xray_metrics_dashboard.png
[4]: https://github.com/jfrog/charts
[5]: https://helm.sh/
[6]: https://app.datadoghq.com/account/settings#api
[7]: https://github.com/jfrog/metrics#setup
[8]: https://www.jfrog.com/confluence/display/JFROG/Access+Tokens#AccessTokens-GeneratingAdminTokens
[9]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7#agent-configuration-directory
[10]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_platform/datadog_checks/jfrog_platform/data/conf.yaml.example
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#restart-the-agent
[12]: https://docs.datadoghq.com/agent/kubernetes/integrations/?tab=kubernetes
[13]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[14]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_platform/metadata.csv
[15]: https://docs.datadoghq.com/help/
