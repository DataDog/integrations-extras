# Agent Check: JFrog Platform Cloud

## Overview

[JFrog][1] is a universal hybrid, end-to-end DevOps platform. JFrog Artifactory is the single solution for housing and managing all the artifacts, binaries, packages, files, containers, and components for use throughout your software supply chain.

JFrog Artifactory serves as your central hub for DevOps, integrating with your tools and processes to improve automation, increase integrity, and incorporate best practices along the way.

JFrog's SaaS Log Streamer is a log streaming solution built by JFrog for SaaS customers. This solution will stream JFrog Artifactory logs from the customer's JFrog SaaS instance straight into their Datadog instance.

Customers who use both JFrog and Datadog will be able to visualize Artifactory logs inside pre-configured Datadog dashboards. This integration also has built-in support for Datadog log pipelines which means logs streamed from JFrog will be pre-processed and automatically converted into the Datadog log format, allowing teams to uniquely name logs per their needs, drill down into Artifactory logs through searchable facets, and monitor their JFrog SaaS instance.

This integration streams the following artifactory logs to Datadog:

- **access-audit.log**
- **artifactory-request.log**
- **access-security-audit.log**

These logs will allow customers to readily know who accessed what repositories and how often. The logs will also show what IP addresses accessed those repositories. Log types such as traffic.log, artifactory-access.log and more request logs will be added to this integration in future updates.

JFrog's SaaS Log Streaming is currently in beta. While in beta, the cloud log streaming feature will only be available inside the MyJFrog portal for select JFrog Enterprise and customers. JFrog plans to GA this feature later in Q2 2024 at which point it will be available to all JFrog Enterprise and customers.

## Setup

**Note:** The integration requires a JFrog Enterprise Plus subscription.

### Installation

1. Create a [Datadog API key][2].
2. On the [MyJFrog Portal][3], go to Settings > JFrog Cloud Log Streaming - BETA, and enable the Log Streamer.
3. Select Datadog as the vendor. 
4. Add your Datadog API key, select the Datadog intake URL for your [Datadog site][4] from the dropdown menu, and add `ddtags` if needed. Click Save.

Your logs will start streaming into Datadog in 24 hours or less.

## Support

Need help? Contact [JFrog Support][5]. 

[1]: https://jfrog.com/
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://my.jfrog.com
[4]: https://docs.datadoghq.com/getting_started/site/
[5]: https://support.jfrog.com/