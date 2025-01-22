## Overview

Reflectiz's innovative agentless solution monitors and detects vulnerabilities in all 1st, 3rd, and 4th party applications within your online ecosystems, offering complete visibility into your web risk exposure surface. It effectively prioritizes and remediates risks and compliance issues using its proprietary exposure rating system.  
With the **Reflectiz Integration** for Datadog, you can elevate your website's security to the next level. This integration introduces the **Web Exposure Rating** and **Web Exposure Alerts** features, enabling you to proactively assess and address potential security risks on your website.  
The integration provides a combination of logs and metrics to support both rating and alerts.

### Features of the integration

- **Web Exposure Rating**: Gain a clear and comprehensive security rating for your website components. The Reflectiz Rating feature provides an at-a-glance evaluation of your website's security status, helping you understand where you stand and where improvements are needed.
- **Web Exposure Alerts**: Be informed in real time about potential risks and vulnerabilities. The integration generates detailed alerts that notify you of misconfigurations, suspicious activity, and emerging threats so that you can take immediate action.
- **Seamless integration with Datadog**: View both the Reflectiz Rating and Risk Alerts directly within your Datadog environment. This allows you to monitor your website's security alongside performance and infrastructure metrics, all in one centralized platform.
- **Prioritize what matters most**: With the Reflectiz Rating and actionable alerts, you can easily identify and prioritize the most critical risks, focusing your efforts on the areas that need attention the most.



## Setup

Follow these steps to integrate Reflectiz with your Datadog account:

### In Datadog

1. Navigate to the **Integrations** tab in Datadog.
2. Find the **Reflectiz** tile and click **Install Integration**.
3. Click **Connect Accounts** to start the authorization process, which redirects you to the Reflectiz Platform.

### In the Reflectiz Platform

1. Enter your Reflectiz credentials to access your account.
2. Choose the appropriate license for the integration.

Once this flow is complete, Web Exposure Alerts and Rating data are available within the included dashboards.

### Link Reflectiz sites with hosts

To make your data more efficient and meaningful, you can link each of your Reflectiz sites to a host in Datadog:

1. Open the Datadog [host list][1].
2. Select a host.
3. Add a tag under the **User tag** section. The tag should follow the format `reflectiz.host.site:{domain}`, where `domain` is Reflectiz site you want to link in the format `example.com`.<br>If you want to add additional sites to a single host, you can add more tags following the format `reflectiz.host.site.1:{domain}`, `reflectiz.host.site.2:{domain}`, and so on.

Once you complete these steps, all Metrics and Logs sent by the Reflectiz integration for the site are related to the host.


## Uninstallation

To uninstall the Reflectiz integration from Datadog:

- From the integration tile, select **Uninstall Integration**. 
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][5].

These steps fully remove the Reflectiz integration from your Datadog account.

## Data Collected

### Logs

The Reflectiz integration sends different types of logs to Datadog, each associated with a specific service. These logs provide detailed insights into scans, app risks, and domain risks, helping you monitor your website's security effectively.

#### Scan logs
- **Log service name**: `reflectiz.v1.scan`
- **Tags**:
  - `reflectiz.site`: The site being scanned.
  - `reflectiz.scan`: The identifier of the scan.
  - `reflectiz.scan.number`: The identifier of the scan as an integer (for more filtering options).

These logs trigger each time a scan is run on a website.

#### Alert logs
- **Log service name**: `reflectiz.v1.alerts`
- **Tags**:
  - `reflectiz.site`: The site being scanned.
  - `reflectiz.scan`: The identifier of the scan.
  - `reflectiz.scan.number`: The identifier of the scan as an integer (for more filtering options).
  - `reflectiz.app`: The app that is related to the alert, if present.
  - `reflectiz.domain`: The domain that is related to the alert, if present.

These logs highlights alerts triggered during the site's scan.


#### Rating scan logs
- **Log service name**: `reflectiz.v1.scan`
- **Tags**:
  - `reflectiz.site`: The site being scanned.
  - `reflectiz.scan`: The identifier of the scan.
  - `reflectiz.scan.number`: The identifier of the scan as an integer (for more filtering options).

These logs trigger each time a scan is run on a website and the ratings are calculated, and they can be useful when filtering the rating data.

#### App risks logs
- **Log service name**: `reflectiz.v1.rating.app.risks`
- **Tags**:
  - `reflectiz.site`: The site being scanned.
  - `reflectiz.scan`: The identifier of the scan.
  - `reflectiz.scan.number`: The identifier of the scan as an integer (for more filtering options).
  - `reflectiz.app`: The application being assessed.

These logs highlight risks related to specific applications on your site, helping you pinpoint vulnerabilities.

#### Domain risks logs
- **Log service name**: `reflectiz.v1.rating.domain.risks`
- **Tags**:
  - `reflectiz.site`: The site being scanned.
  - `reflectiz.scan`: The identifier of the scan.
  - `reflectiz.scan.number`: The identifier of the scan as an integer (for more filtering options).
  - `reflectiz.domain`: The domain being assessed.

These logs focus on risks related to domains, providing a clear picture of domain-specific vulnerabilities.


### Metrics
See [metadata.csv][add link] for a list of metrics provided by this integration.

## Support
For support or feature requests, contact Reflectiz through the following channels:

- Support: [support@reflectiz.com][2]
- Sales: [inbound@reflectiz.com][3]
- Website: [reflectiz.com][4]

[1]: https://app.datadoghq.com/infrastructure
[2]: mailto:support@reflectiz.com
[3]: mailto:inbound@reflectiz.com
[4]: https://reflectiz.com
[5]: https://app.datadoghq.com/organization-settings/api-keys?filter=Reflectiz