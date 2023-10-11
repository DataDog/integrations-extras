# Agent Check: JFrog Platform Cloud

## Overview

[JFrog][1] is a universal hybrid, end-to-end DevOps platform. JFrog Artifactory is the single solution for housing and managing all the artifacts, binaries, packages, files, containers, and components for use throughout your software supply chain.
JFrog Artifactory serves as your central hub for DevOps, integrating with your tools and processes to improve automation, increase integrity, and incorporate best practices along the way.

JFrog’s SaaS Log Streamer is a log streaming solution built by JFrog for SaaS customers. This solution will stream JFrog Artifactory logs from the customer’s JFrog SaaS instance straight into their Datadog cloud instance.

Customers who use both JFrog and Datadog will be able to visualize Artifactory logs inside pre-configured Datadog dashboards. This integration also has built-in support for Datadog log pipelines which means logs streamed from JFrog will be preprocessed and automatically converted into Datadog log format and allow teams to uniquely name logs per their needs.This integration will thus make it easy and convenient for customers to monitor their JFrog SaaS instance.

At the initial release this integration will stream the following artifactory logs to datadog:

- **access-audit.log**
- **artifactory-request.log**
- **access-security-audit.log**

These logs will allow customers to readily know who accessed what repositories and how often. The logs will also show what IP addresses accessed those repositories. The logs are critical for customers from a security and compliance perspective. In future updates to this integration JFrog will be adding many more log types like traffic.log, artifactory-access.log and more request logs.

## Setup

### Installation

Contact [JFrog Partners team](mailto:partner-support@jfrog.com) to enable the integration for your cloud instance. Be ready to provide your [Datadog API key][2].

## Support

Need help? Contact [JFrog Support][3].

[1]: https://jfrog.com/
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://support.jfrog.com/

