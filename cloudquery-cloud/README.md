# CloudQuery Cloud

![datadog-integration][1]

## Overview

[CloudQuery][2] is an open-source, high-performance data integration framework built for developers, with support for a wide range of plugins.

CloudQuery extracts, transforms, and loads configuration from cloud APIs to a variety of supported destinations such as databases, data lakes, or streaming platforms for further analysis.

[CloudQuery Cloud][3] is a great way to get started with CloudQuery and syncing data from source to destination without the need to deploy your own infrastructure. It is also much easier to connect to sources and destinations with the integrated OAuth authentication support. You only need to select a source and destination plugin and CloudQuery will take care of the rest.

## Setup

### Installation

Sign up for free at [cloud.cloudquery.io][3]. Once logged in, navigate to the **Sources** page and add a Datadog source. Under the **Authentication** section, use the **Authenticate** button to grant access to your Datadog account using OAuth2 flow.

For more information about using CloudQuery Cloud, refer to the [quickstart guide][4].

### Configuration

Detailed documentation for the CloudQuery Datadog source is available [here][5].

## Uninstallation

Navigate to the **Sources** page under [CloudQuery Cloud][3] and find your Datadog source you have previously set up. Under the **Edit source** tab, click the **Delete this source** button.

## Support

For support, contact [CloudQuery][2] or [CloudQuery Community][6].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/cloudquery/images/cloudquery_logo_png_dark_background.png
[2]: https://www.cloudquery.io/
[3]: https://cloud.cloudquery.io/
[4]: https://docs.cloudquery.io/docs/quickstart/cloudquery-cloud
[5]: https://hub.cloudquery.io/plugins/source/cloudquery/datadog/latest/docs
[6]: https://community.cloudquery.io/
