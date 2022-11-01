## Overview
The following describes how to configure Datadog to gather Metrics and Logs from JFrog Artifactory and JFrog Xray.

### JFrog Artifactory and Xray
JFrog Enterprise with Xray features Artifactory Enterprise and Xray. Together, they empower DevOps teams to improve their productivity to increase velocity and deliver high quality software releases with confidence. 

Artifactory supports multiple build packages, artifacts, and metadata. It allows DevOps teams to have the freedom of choice of build packages like Bower, Chef, CocoaPods, Conan, Conda, CRAN, Debian, Docker, Golang, Gradle, Git LFS, Helm, Ivy, Maven, npm, NuGet, Opkg, P2, PHP Composer, Puppet, PyPI, RPM, RubyGems, SBT, Vagrant & VCS, CI/CD platforms, and devops tools.

Artifactory Enterprise supports multi-region, multi-cloud, and hybrid replication for geographically distributed teams allowing you to replicate between a source repository and multiple targets simultaneously and security features such as IP filtering, CNAME, and data encryption at rest. Artifactory supports Kubernetes for microservices and containerized applications. Manage your deployments and gain insight into dependencies using Artifactory as your Kubernetes registry. 

JFrog Xray is a continuous security and universal artifact analysis solution that provides multi-layered analysis of your containers and software artifacts for vulnerabilities and license compliance issues. It is the only Software Composition Analysis solution that natively integrates with JFrog Artifactory for optimized scanning and unified operation. Supports all major package types, understands how to unpack them, and uses recursive scanning to see into all of the underlying layers and dependencies, even those packaged in Docker images, and zip files.

### JFrog Artifactory and Xray logs Datadog dashboard

The JFrog Datadog integration allows you to send Artifactory/Xray logs to the log stream in Datadog. You can use it to enhance your existing dashboards or to gain more insight into JFrog Artifactory's usage statistics or JFrog Xray's scanned components details.

![dashboard][1]

![dashboard][16]

![dashboard][17]

### JFrog Artifactory and Xray metrics API dashboard

JFrog Artifactory and Xray metrics API integration with Datadog allows you to send metrics from the OpenMetrics API endpoint to Datadog. With this integration, you can gain insights into the system performance, storage consumption, and connection statistics associated with JFrog Artifactory/Xray, as well as, insights into the count and type of artifacts and components scanned by Xray. After setting up the configuration, these metrics are available as out-of-the-box dashboards and may be used to enhance existing dashboards within Datadog.

![artifactory][2]

![xray][3]

## Setup


### Metrics collection

1. Enable Metrics for Artifactory and Xray:

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
    2. [Restart the Agent][11]. For containerized environments, see the [Autodiscovery Integration Templates][12] for guidance on applying the parameters specified above. To validate that the changes are applied, [run the Agent's status subcommand][13] and look for `openmetrics` under the Checks section.

### Log collection - Using FluentD

#### Requirements

* Your [Datadog API key][6].

#### Setup and Configure
1. Install Fluentd using the [jFrog documentation][18] based on your installation type, and define the environment variable.

2. Configure Fluentd with Artifactory by downloading the Artifactory Fluentd configuration file to a directory you have permissions to write in, such as `$JF_PRODUCT_DATA_INTERNAL` locations.
    
    ```text
    cd $JF_PRODUCT_DATA_INTERNAL
    wget https://raw.githubusercontent.com/jfrog/log-analytics-datadog/master/fluent.conf.rt
    ```
    
    Override the match directive (last section) of the downloaded `fluent.conf.rt` with the details given below:
    
    ```
    <match jfrog.**>
      @type datadog
      @id datadog_agent_jfrog_artifactory
      api_key API_KEY
      include_tag_key true
      dd_source fluentd
    </match>
    ```
    
    - `API_KEY` (required) is the API key from [Datadog][4].
    - `dd_source` is the name of the log integration in your logs in order to trigger the integration automatic setup in datadog.
    - `include_tag_key` defaults to false and adds the `fluentd` tag in the JSON record if set to true.

3. Configure Fluentd with Xray by downloading the Xray Fluentd configuration file to a directory you have permissions to write, such as the `$JF_PRODUCT_DATA_INTERNAL` locations.
    
    ```text
    cd $JF_PRODUCT_DATA_INTERNAL
    wget https://raw.githubusercontent.com/jfrog/log-analytics-datadog/master/fluent.conf.xray
    ```
    
    Fill in the `JPD_URL`, `USER`, `JFROG_API_KEY` fields in the source directive of the downloaded `fluent.conf.xray` with the details given below:
    
    ```text
    <source>
      @type jfrog_siem
      tag jfrog.xray.siem.vulnerabilities
      jpd_url JPD_URL
      username USER
      apikey JFROG_API_KEY
      pos_file "#{ENV['JF_PRODUCT_DATA_INTERNAL']}/log/jfrog_siem.log.pos"
    </source>
    ```
    
    * `JPD_URL` (required) is the Artifactory JPD URL of the format `http://<ip_address>`, which is used to pull Xray Violations.
    * `USER` (required) is the Artifactory username for authentication.
    * `JFROG_API_KEY` (required) is the [Artifactory API Key][19] for authentication.
    
    Override the match directive (last section) of the downloaded `fluent.conf.xray` with the details given below:
    
    ```
    <match jfrog.**>
      @type datadog
      @id datadog_agent_jfrog_xray
      api_key API_KEY
      include_tag_key true
      dd_source fluentd
    </match>
    ```
    
    * `API_KEY`  (required) is the API key from [Datadog][4].
    * `dd_source` is the name of the log integration in your logs in order to trigger the integration automatic setup in Datadog.
    * `include_tag_key` defaults to false and adds the `fluentd` tag in the json record if set to true.
    
4. Enable the integration by running `td-agent` on `artifactory` and `xray` instances:

    ``` 
    td-agent
    ```

    The API key is configured in `td-agent`, which starts sending logs to Datadog. For other types of installation, see the [JFrog documentation][18].

    Add all attributes as facets from **Facets** > **Add** (on the left side of the screen in Logs) > **Search**.


### JFrog platform tile 

If you have not installed the JFrog platform tile yet, install the tile.

### JFrog dashboards

Go to Dashboard -> Dashboard List, find `JFrog Artifactory Dashboard`, `Artifactory Metrics`, `Xray Metrics`, `Xray Logs`, `Xray Violations` and explore it.

### Data Collected

#### Metrics

See [metadata.csv][14] for a list of metrics provided by this check.

## Troubleshooting

Need help? Contact [Datadog support][15].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/dashboard.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/artifactory_metrics_dashboard.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/xray_metrics_dashboard.png
[4]: https://docs.datadoghq.com/account_management/api-app-keys/
[5]: https://helm.sh/
[6]: https://app.datadoghq.com/organization-settings/api-keys
[7]: https://github.com/jfrog/metrics#setup
[8]: https://www.jfrog.com/confluence/display/JFROG/Access+Tokens#AccessTokens-GeneratingAdminTokens
[9]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7#agent-configuration-directory
[10]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_platform/datadog_checks/jfrog_platform/data/conf.yaml.example
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#restart-the-agent
[12]: https://docs.datadoghq.com/agent/kubernetes/integrations/?tab=kubernetes
[13]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[14]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_platform/metadata.csv
[15]: https://docs.datadoghq.com/help/
[16]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/xray_logs.png
[17]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/xray_violations.png
[18]: https://github.com/jfrog/log-analytics-datadog/blob/master/README.md
[19]: https://www.jfrog.com/confluence/display/JFROG/User+Profile#UserProfile-APIKey
[20]: https://docs.datadoghq.com/agent/logs/?tab=tailfiles#activate-log-collection
[21]: https://docs.datadoghq.com/agent/logs/advanced_log_collection/?tab=configurationfile#tail-directories-by-using-wildcards
