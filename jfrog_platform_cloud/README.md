# Agent Check: JFrog Platform Cloud

## Overview

[JFrog](https://jfrog.com/) is a universal hybrid, end-to-end DevOps platform. JFrog Artifactory is the single solution for housing and managing all the artifacts, binaries, packages, files, containers, and components for use throughout your software supply chain.
JFrog Artifactory serves as your central hub for DevOps, integrating with your tools and processes to improve automation, increase integrity, and incorporate best practices along the way.

JFrog's SaaS Log Streamer is a log streaming solution built by JFrog for SaaS customers. This solution will stream JFrog Artifactory logs from the customer's JFrog SaaS instance straight into their Datadog instance.

Customers who use both JFrog and Datadog will be able to visualize Artifactory logs inside pre-configured Datadog dashboards. This integration also has built-in support for Datadog log pipelines which means logs streamed from JFrog will be preprocessed and automatically converted into the Datadog log format, allowing teams to uniquely name logs per their needs, drill down into Artifactory logs through searchable facets, and easily monitor their JFrog SaaS instance.

At the initial release this integration will stream the following artifactory logs to Datadog:

- **access-audit.log**
- **artifactory-request.log**
- **access-security-audit.log**

These logs will allow customers to readily know who accessed what repositories and how often. The logs will also show what IP addresses accessed those repositories. Log types such as traffic.log, artifactory-access.log and more request logs will be added to this integration in future updates.

## Setup

**Note:** The integration requires JFrog Enterprise Plus subscription. 

### Installation

Create [DataDog API key](https://app.datadoghq.com/organization-settings/api-keys).  

On the [MyJFrog Portal](https://my.jfrog.com), go to Settings -> JFrog Cloud Log Streaming - BETA, and enable the Log Streamer.
Select Datadog as the vendor. Add your Datadog API key, the Datadog intake URL for your [Datadog site](https://docs.datadoghq.com/getting_started/site/) (`https://http-intake.logs.datadoghq.com/api/v2/logs`), and `ddtags`. Click Save.
Your logs will start streaming into Datadog in 24 hours or less.

## Support

Need help? Contact [JFrog Support](https://support.jfrog.com/).