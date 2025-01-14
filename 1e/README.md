# 1E

## Overview

At [1E][1], we reimagine how technology serves people and create new ways for IT to shape the future of work.

The 1E platform helps IT teams improve end user experience, tighten security, reduce costs, and evolve IT Operations from cost center to strategic enabler.
Our platform contains 1E for Visibility, Control, and Compliance, 1E for Digital Experience Observability, and 1E for Service Desk Automation solutions.

The 1E Datadog Integration is an API-based integration that collects metrics from 1E products and forwards them to your Datadog account.

Integrating Datadog with 1E enables IT administrators to:

- View device data and related information in one place in Datadog.
- View Digital Employee Experience (DEX) score and related information.
- Build a customizable dashboard inside Datadog for customer specific insights.

## Setup

### Prerequisites

To configure your integration between Datadog and 1E you will need to have the following in place:

- 1E 8.4 installed. At least one 1E client must be connected to provide metrics data.
- A user that is assigned to the **Full Administrator** role.
- 1E PowerShell Toolkit 2.0 or later, which is available from the [1E Support portal][2].
- In Datadog, a user that is assigned to the **Datadog Admin** role who can download the 1E Dashboard from the Marketplace.

### Configuration

#### Creating a Datadog API Key

To set up the integration with 1E, create a Datadog API key, and then upload the API key and site URL to 1E using the 1E API.

1. Navigate to the **Organization Settings** > [**API Keys**][3] page and create an API key.
2. Identify your [Datadog site URL][4]. You will need this information when adding the Datadog configuration to 1E.

#### Adding the Datadog configuration to 1E

To update the Global Settings table in the 1E Master database, use the 1E API with the 1E PowerShell Toolkit (recommended) or Postman.

##### Using 1E PowerShell Toolkit to upload your Datadog configuration

Download and install the 1E PowerShell Toolkit, if you have not already done so. To install and use the toolkit, refer to the [1E documentation][8].

You will need to run the PowerShell Toolkit command similar to:

```powershell
Add-TachyonAxmDatadogConfiguration `
-DatadogKey YOUR_DATADOG_API_KEY `
-DatadogSite https://app.datadoghq.eu/ `
-Enable $true
```

Parameters:

- `DatadogKey`: Specifies the Datadog API key required for authentication.
- `DatadogSite`: Specifies the Datadog Site URL.
- `Enable`: Enables or disables the Datadog integration. The default value is `true`.

##### Using Postman to upload your Datadog configuration

As an alternative to using the 1E PowerShell Toolkit command, you can use [Postman][7] to upload your Datadog configuration.

The following are the equivalent cURL commands:

```bash
curl --location --request POST 'https://tcnsvr.vmdc.local/consumer/
Settings' \
--header 'x-tachyon-authenticate: ********' \
--header 'X-Tachyon-Consumer: PatchInsights' \
--header 'Content-Type: application/json' \
--data-raw '{
 "Name": "AxmDatadogConfiguration",
 "Usage": 0,
 "Value": "{ \"ApiKey\":\"YOUR_DATADOG_API_KEY\",
\"SiteName\":\"https://app.datadoghq.eu/\" }"
}'
curl --location --request POST 'https://tcnsvr.vmdc.local/consumer/
Settings' \
--header 'x-tachyon-authenticate: ********' \
--header 'X-Tachyon-Consumer: PatchInsights' \
--header 'Content-Type: application/json' \
--data-raw '{
 "Name": "EnableAxmDatadogIntegration",
 "Usage": 0,
 "Value": "false"
}'
```

### Verify

Install the 1E Dashboard integration if you have not already done so, and then open the 1E Dashboard.

If the integration has been configured correctly, the dashboard will show data in each tile. If this is your first time installing 1E, you will have to wait for 1E to finish processing metrics, which happens once every 24 hours (by default this starts at midnight UTC).

If you are familiar with using 1E, you can confirm data is available in the **Experience Analytics** app in the 1E portal. Note you must sign in as a user that is assigned in 1E to either the **Full Administrator** role or **Experience Viewers** role.

Refer to the [Datadog documentation][5] for more details about creating, adding, and customizing your dashboards.

### Using 1E Dashboard

You can use the 1E Dashboard to view digital employee experience scores, trends, and device metrics reported by 1E in Datadog. Experience data helps you visualize your end-users' experience of IT service delivery across your enterprise.

Once you have the 1E Dashboard, you can view 1E metrics such as the following:

- Application crashes
- Application hangs
- Service failures
- OS reboots
- OS Upgrades
- Software installations and uninstalls
- Patch installations and uninstalls.

In addition, you can view data about:

- Number of connected devices
- Digital Employee Experience (DEX) score related to:
  - Performance
  - Stability
  - Responsiveness
  - Sentiment.

### Schedule reports and create notifications in Datadog

Once you have configured the 1E Dashboard, you have the option to schedule reports and create
notifications from it. Refer to the [Datadog documentation][5] for details.

## Data Collected

### Metrics

See [metadata.csv][9] for a list of metrics provided by this integration.

### Service Checks

The 1E integration does not include any service checks.

### Events

The 1E integration does not include any events.

## Troubleshooting

Need help? Contact [1E Support][1].

[1]: https://www.1e.com/
[2]: https://1eportal.force.com/s/
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://docs.datadoghq.com/getting_started/site/
[5]: https://docs.datadoghq.com/
[6]: https://docs.datadoghq.com/help/
[7]: https://www.postman.com/
[8]: https://help.1e.com/TCN81/en/736741-764706-using-the-1e-powershell-toolkit.html
[9]: https://github.com/DataDog/integrations-extras/blob/master/1e/metadata.csv
