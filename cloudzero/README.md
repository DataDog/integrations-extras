# Agent Check: CloudZero

## Overview

CloudZero helps engineering teams build cost-effective software. Use its platform to allocate 100% of your cloud, PaaS, and SaaS cost-regardless of tagging quality-and present it in a single unified view. Combine hourly cost data with business- and system-level telemetry to put cloud data in a business context through precise unit cost metrics like cost per customer, per product, per feature, per team, and more. CloudZero's AI-powered anomaly detection alerts engineers to abnormal spend events by pointing them directly to the affected infrastructure, and promotes engineering engagement in cloud cost management.

### Benefits

Once connected, the CloudZero platform regularly ingests your Datadog billing information for both committed and on-demand costs across all Datadog products. CloudZero unifies this data with the rest of your cloud costs, giving you a comprehensive assessment of your total cloud investment. The platform then puts all of your cloud spend through numerous analytics features, revealing opportunities for efficiency and letting you craft and send custom reports.

## Setup

### Installation

Click **Install Integration** on the [Datadog integration tile][2]. Once the integration is installed, click **Connect Accounts** under the **Configure** tab to authorize CloudZero to access your Datadog account. This will take you to the CloudZero application where you will create a connection adding a name and selecting the site to which your parent Datadog account is assigned.

Once a connection is created, click **Continue** to authorize CloudZero to pull data from your Datadog account into the CloudZero platform.

### Configuration

You can adjust settings from the connection details page for your Datadog connection in CloudZero.

### Validation

1. From the list of [connections][3], you can see the status of your connection to Datadog.
2. Click on the name of your Datadog connection to view more details about the amount and timing of data that has been pulled from Datadog.
3. Once data ingestion has successfully run, see Datadog costs included in the [Cost Explorer][4].

## Uninstallation

- Once this integration has been uninstalled, any previous authorizations are revoked.
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][5].

## Troubleshooting

Need help? Contact [CloudZero support][6].

[1]: https://app.cloudzero.com
[2]: https://app.datadoghq.com/integrations/cloudzero
[3]: https://app.cloudzero.com/organization/connections
[4]: https://app.cloudzero.com/explorer
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: mailto:support@cloudzero.com
