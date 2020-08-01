# Artifactory and Xray Logging Analytics with Datadog

## Overview

The following describes how to configure Datadog to gather metrics from Artifactory and Xray.

## Requirements

* Kubernetes Cluster
* Artifactory and/or Xray installed via [JFrog Helm Charts](https://github.com/jfrog/charts)
* Helm 3

## Datadog Setup

Datadog setup can be done by creating an account in datadog and going through onboarding steps or by using apiKey directly if one exists

* Run the datadog agent in your kubernetes cluster by deploying it with a helm chart
* To enable log collection, update datadog-values.yaml file given in the onboarding steps
* Once the agent starts reporting, you'll get an apiKey which we'll be using to send formatted logs through fluentd

Once datadog is setup, we can access logs via Logs > Search. We can also select the specific source that we want to get logs from

If an apiKey exists, use the Datadog Fluentd plugin to forward logs directly from Fluentd to your datadog account. 
Adding proper metadata is the key to unlocking the full potential of your logs in datadog. By default, the hostname and timestamp fields should be remapped

### FluentD Configuration

Integration is done by specifying the apiKey

_api_key_ is the apiKey from datadog

_dd_source_ attribute is set to the name of the log integration in your logs in order to trigger the integration automatic setup in datadog.

_include_tag_key_ defaults to false and it will add fluentd tag in the json record if set to true

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

To run this integration start by running td-agent on artifactory and xray pods

``` 
td-agent
```

The apiKey is configured in td-agent which will start sending logs to datadog. 

Add all attributes as facets from Facets > Add on the left side of the screen in Logs > search

To access already existing visualizations and filters, click on Dashboards and add a new screenboard and then import [export.json](https://github.com/jfrog/log-analytics/blob/master/datadog/export.json) and overwrite the existing dashboard

## Generating Data for Testing
[Partner Integration Test Framework](https://github.com/jfrog/partner-integration-tests) can be used to generate data for metrics.

## References
* [Datadog](https://docs.datadoghq.com/getting_started/) - Cloud monitoring as a service
