# 1E

## Overview

At [1E][1], we reimagine how technology serves people and create new ways for IT to shape the future of work.

The 1E Datadog Integration is an API-based integration that collects metrics from 1E products and forwards them to your Datadog account.

Integrating Datadog with 1E enables IT administrators to:

- View device data and related information in one place in Datadog
- View Digital Employee Experience (DEX) score and related information
- Build a customizable dashboard inside Datadog for customer specific insights.

## Setup

### Prerequisites

To configure your integration between Datadog and 1E you will need to have the following in place:

- 1E 8.4
  - platform installed, with at least one 1E client connected to provide metrics data
  - a user that is assigned to the **Full Administrator** role
  - 1E PowerShell Toolkit 2.0 or later, available from the [1E Support portal][2]
- Datadog
  - a user that is assigned to the **Datadog Admin** role and able to download the 1E Dashboard from the Marketplace.

### Configuration

Steps required to configure your integration between Datadog and 1E.

#### Installing the 1E Dashboard

You can install the 1E Dashboard from the Datadog Marketplace at any time in this process.

To install, navigate to **Integrations** in your Datadog instance, search for **1E**, and open **1E Dashboard**.

In 1E Dashboard, click on **Install Integration**.

The dashboard's tiles will show data after you have configured integration with 1E.

#### Creating a Datadog API Key

To set up the integration with 1E, you need to upload a Datadog API key and site URL to your 1E
installation, using the 1E PowerShell Toolkit or Postman.

1. To get started, go to the [Datadog APIs page][3], where you can create an API key

2. Determine your [Datadog API site URL][4] with reference to Datadog documentation

#### Adding the Datadog configuration to 1E

These steps tell 1E about the Datadog API key and site URL that you obtained in the previous step, by using a 1E API to update the Global Settings table in the 1E Master database.

##### Using 1E PowerShell Toolkit to upload your Datadog configuration

First, you will need to download and install the 1E PowerShell Toolkit, if you have not already done so. To install and use the toolkit, please refer to 1E online documentation at https://help.1e.com/display/TCNSDK/Tachyon+PowerShell+Toolkit.

You will need to run the PowerShell Toolkit command similar to:

```powershell
Add-TachyonAxmDatadogConfiguration `
-DatadogKey YOUR_DATADOG_API_KEY `
-DatadogSite https://app.datadoghq.eu/ `
-Enable $true
```

Parameters:

- _DatadogKey_ - specifies the Datadog API key required for authentication
- _DatadogSite_ - specifies the Datadog Site URL
- _Enable_ - enables or disables Datadog integration, the default value is true.

##### Using Postman to upload your Datadog configuration

An alternative to using the 1E PowerShell Toolkit command, you could also use Postman to upload your Datadog configuration, if you are familiar with this tool. You can find more details about Postman at https://www.postman.com/.

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

Install the 1E Dashboard integration if you have not already done so.

Open the 1E Dashboard.

If integration has been configured correctly, the dashboard will show data in each tile. If you have only just installed 1E, then you will have to wait for 1E to complete processing metrics, which happens once every 24 hours (by default this starts at midnight UTC).

If you are familiar with using 1E, then you can confirm data is available by signing in to the 1E portal and viewing in the **Experience Analytics** app. You need to sign in as a user that is assigned in 1E to either the **Full Administrator** role or **Experience Viewers** role.

Please refer to [Datadog documentation][5] for more details about creating, adding, and customizing your dashboards.

### Using 1E Dashboard

You can use the 1E Dashboard to view digital employee experience scores, trends and device metrics reported by 1E in Datadog. Experience data helps you visualize your end-users' experience of IT service delivery across your enterprise.

Once you have the 1E Dashboard, you can view 1E metrics like:

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
notifications from it.
Refer to the [Datadog documentation][5] for details.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this integration.

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
