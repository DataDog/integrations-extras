# CloudQuery Cloud

## Overview

[CloudQuery][1] is an open-source, high-performance data integration framework built for developers, with support for a wide range of plugins.

CloudQuery extracts, transforms, and loads configuration from cloud APIs to a variety of supported destinations such as databases, data lakes, or streaming platforms for further analysis.

[CloudQuery Cloud][2] is a great way to get started with CloudQuery and syncing data from source to destination without the need to deploy your own infrastructure. It is also much easier to connect to sources and destinations with the integrated OAuth authentication support. You only need to select a source and destination plugin and CloudQuery will take care of the rest.

## Setup

### Installation

1. Sign up for free at [cloud.cloudquery.io][2]. 
2. In Datadog, navigate to the CloudQuery Cloud integration tile
3. Click **Connect Accounts**
4. You'll be redirected to CloudQuery to log in
5. Navigate to the **Sources** page and add a Datadog source
6. Under the **Authentication** section, use the **Authenticate** button to grant access to your Datadog account using OAuth2 flow.

For more information about using CloudQuery Cloud, refer to the [quickstart guide][3].

### Configuration

Detailed documentation for the CloudQuery Datadog source is available [here][4].

## Uninstallation

1. Navigate to the **Sources** page under [CloudQuery Cloud][2] and find your Datadog source you have previously set up. 
2. Under the **Edit source** tab, click the **Delete this source** button.

## Support

For support, contact [CloudQuery][1] or [CloudQuery Community][5].

[1]: https://www.cloudquery.io/
[2]: https://cloud.cloudquery.io/
[3]: https://docs.cloudquery.io/docs/quickstart/cloudquery-cloud
[4]: https://hub.cloudquery.io/plugins/source/cloudquery/datadog/latest/docs
[5]: https://community.cloudquery.io/
