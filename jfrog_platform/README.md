

## Overview
The following describes how to configure Datadog to gather metrics from JFrog Artifactory and JFrog Xray.

### What is JFrog Artifactory and Xray
JFrog Enterprise with Xray features Artifactory Enterprise and Xray. Together, they empower DevOps teams to improve their productivity to increase velocity and deliver high quality software releases with confidence. Xray scans for known open source security risks and compliance using the industry's most comprehensive intelligence, VulnDB.

Artifactory supports multiple build packages, artifacts, and metadata. It allows DevOps teams to have the freedom of choice of build packages like Bower, Chef, CocoaPods, Conan, Conda, CRAN, Debian, Docker, Golang, Gradle, Git LFS, Helm, Ivy, Maven, npm, NuGet, Opkg, P2, PHP Composer, Puppet, PyPI, RPM, RubyGems, SBT, Vagrant & VCS, CI/CD platforms, and devops tools.

Artifactory Enterprise supports multi-region, multi-cloud, and hybrid replication for geographically distributed teams allowing you to replicate between a source repository and multiple targets simultaneously and security features such as IP filtering, CNAME, and data encryption at rest.

Artifactory supports Kubernetes for microservices and containerized applications. Manage your deployments and gain insight into dependencies using Artifactory as your Kubernetes registry. JFrog Xray provides container security scanning all layers recursively, ensuring that every artifact and dependency included in your Docker image has been scanned for known risks. Enterprise meets your business model needs supporting hybrid, cloud, and multi-cloud environments.

### JFrog Artifactory Datadog Dashboard

JFrog Artifactory's Datadog integration allows you to send Artifactory logs to the log stream in Datadog. You can use it to enhance your existing dashboards or to gain more insight into Artifactory's usage statistics.

![dashboard][3]

## Setup

### Requirements

* Kubernetes Cluster
* JFrog Artifactory and/or JFrog Xray installed via [JFrog Helm Charts][1]
* [Helm 3][2]

### Logs

Datadog setup can be done by creating an account in Datadog and going through these onboarding steps or by using the API key directly.

* Run the Datadog Agent in your Kubernetes cluster by deploying it with a Helm chart
* To enable log collection, update the `datadog-values.yaml` file given in the onboarding steps
* Once the Agent starts reporting, you'll get an API key which we'll be using to send formatted logs through fluentd

Once Datadog is setup, we can access logs in the UI under  **Logs** > **Search**. Select the specific source that to retrieve logs.

If an API key exists, use the Datadog Fluentd plugin to forward logs directly from Fluentd to your Datadog account. 
Adding proper metadata is the key to unlocking the full potential of your logs in Datadog. By default, the hostname and timestamp fields should be remapped.

### Fluentd Configuration

Integration is done by specifying the API key

_api_key_ is the API key from Datadog

_dd_source_ attribute is set to the name of the log integration in your logs in order to trigger the integration automatic setup in Datadog.

_include_tag_key_ defaults to false and it will add fluentd tag in the JSON record if set to true

```
<match jfrog.**>
  @type datadog
  @id datadog_agent_artifactory
  api_key <api_key>
  include_tag_key true
  dd_source fluentd
</match>
```

## Datadog Demo

To enable this integration, run the td-agent on `artifactory` and `xray` pods

``` 
td-agent
```

The API key is configured in `td-agent`, which will start sending logs to Datadog. 

Add all attributes as facets from **Facets** > **Add** (on the left side of the screen in Logs) > **Search**.

To access already existing visualizations and filters, click on Dashboards and add a new screenboard and then import [export.json][4] and overwrite the existing dashboard.


[1]: https://github.com/jfrog/charts
[2]: https://helm.sh/
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/jfrog_platform/images/dashboard.png
[4]: https://github.com/jfrog/log-analytics/blob/master/datadog/export.json
