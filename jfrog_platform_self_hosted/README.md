<div class="alert alert-warning">The existing agent check to gather JFrog metrics has been replaced with Fluentd. The agent check is deprecated.</div>

## Overview

[JFrog][1] is a universal, hybrid, and end-to-end DevOps platform. This integration helps any JFrog self-hosted customer seamlessly stream logs, violations and metrics from JFrog Artifactory and JFrog Xray straight into Datadog. This integration comes packaged with Datadog [log pipelines][2] which enrich and index logs to make them more searchable and treatable using Datadog [facets][3].  

Let JFrog know how we can improve the integration. Feel free to visit [our GitHub][4] for more detailed documentation.

### JFrog dashboards

You can find the dashboards packaged with this integration under the Assets tab on the integration tile.

#### JFrog Artifactory dashboard
This dashboard is divided into three sections: Application, Audit and Requests.
* **Application** - This section tracks Log Volume (information about different log sources) and Artifactory Errors over time (bursts of application errors that may otherwise go undetected).
* **Audit** - This section tracks audit logs that help you determine who is accessing your Artifactory instance and from where. These can help you track potentially malicious requests or processes (such as CI jobs) using expired credentials.
* **Requests** - This section tracks HTTP response codes and the top 10 IP addresses for uploads and downloads.

#### JFrog Artifactory Metrics dashboard
This dashboard tracks Artifactory System Metrics, JVM memory, Garbage Collection, Database Connections, and HTTP Connections metrics.

#### JFrog Xray Logs dashboard
This dashboard provides a summary of access, service and traffic log volumes associated with Xray. Additionally, customers are also able to track various HTTP response codes, HTTP 500 errors, and log errors for greater operational insight.

#### JFrog Xray Violations dashboard
This dashboard provides an aggregated summary of all the license violations and security vulnerabilities found by Xray. Information is segmented by watch policies and rules. Trending information is provided on the type and severity of violations over time, as well as insights on most frequently occurring CVEs, top impacted artifacts and components.

#### JFrog Xray Metrics dashboard
This dashboard tracks System Metrics and data metrics about Scanned Artifacts and Scanned Components.

## Setup

### Requirements

* Your [Datadog API key][5].
* Install the JFrog Platform (Self-hosted) integration.

### Fluentd Installation
We recommend following the installation guide that matches your environment:

* [OS / Virtual Machine][8]
* [Docker][9]
* [Kubernetes Deployment with Helm][10]

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Events

The JFrog check does not include any events.

### Service Checks

The JFrog check does not include any service checks.

## Support

Need help? Contact [support@jfrog.com](support@jfrog.com) or open a support ticket on JFrog [Customer Support Portal][7]

### Troubleshooting

**Q : I am about to upgrade from on-prem to JFrog Cloud. Can I expect all the same logs to stream into Datadog from my SaaS instance post-migration when I install the SaaS version of the integration?**

A: At launch, the SaaS version of the integration will only stream the artifactory-request, access-audit and access-security-audit logs from your SaaS JFrog instance to Datadog.


[1]: https://jfrog.com/
[2]: https://docs.datadoghq.com/logs/log_configuration/pipelines/?tab=source
[3]: https://docs.datadoghq.com/logs/explorer/facets/
[4]: https://github.com/jfrog/log-analytics-datadog
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: https://github.com/DataDog/integrations-extras/blob/master/jfrog_platform/metadata.csv
[7]: https://support.jfrog.com/s/login/?language=en_US&ec=302&startURL=%2Fs%2F
[8]: https://github.com/jfrog/log-analytics-datadog#os--virtual-machine
[9]: https://github.com/jfrog/log-analytics-datadog#docker
[10]: https://github.com/jfrog/log-analytics-datadog#kubernetes-deployment-with-helm
