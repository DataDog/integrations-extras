## Overview

Take your website's security monitoring to the next level with the **Reflectiz Integration** for Datadog. This powerful integration delivers two essential features: **Web Exposure Rating** and **Web Exposure Alerts**, giving you the tools to assess and respond to potential security risks on your website.

### Why This Integration is Essential for You

1. **Web Exposure Rating: Know Your Security Posture**  
   Gain a clear and comprehensive security rating for your website components. The Reflecting Rating feature provides an at-a-glance evaluation of your website's security status, helping you understand where you stand and where improvements are needed.

2. **Web Exposure Alerts: Stay Ahead of Threats**  
   Be informed in real-time about potential risks and vulnerabilities. The integration generates detailed alerts that notify you of misconfigurations, suspicious activity, or emerging threats, so you can take immediate action.

3. **Seamless Integration in Datadog**  
   View both the Reflecting Rating and Risk Alerts directly within your Datadog environment. This allows you to monitor your website's security alongside performance and infrastructure metrics, all in one centralized platform.

4. **Prioritize What Matters Most**  
   With the Reflecting Rating and actionable alerts, you can easily identify and prioritize the most critical risks, focusing your efforts on the areas that need attention the most.

---

This integration simplifies your security monitoring by providing two essential features—**Web Exposure Rating** and **Web Exposure Alerts**—to ensure you have the insights and notifications you need to keep your website safe, all from within Datadog.



## Setup

Follow these steps to integrate Reflecting Rating with your Datadog account:

### In Datadog

1. **Navigate to Integrations**:  
   Go to the **Integrations** section in your Datadog dashboard.
 
2. **Install the Reflecting Integration**:  
   Find the **Reflectiz** tile and click **Install Integration**.

3. **Authorize the Integration**:  
   Click **Connect Accounts** to start the authorization process. You will be redirected to the Reflectiz Platform.

### In Reflectiz Platform

1. **Log In**:  
   Enter your Reflectiz credentials to access your account.

2. **Select Your License**:  
   Choose the appropriate license for the integration.

Once these steps are completed, your Reflectiz Dashboards will be available in Datadog.

### Link the Hosts

To make your data more efficient and meaningful you can link each of your reflectiz sites to a host in datadog, to do so follow these simple steps:  

1. Open the [Host list](https://app.datadoghq.com/infrastructure) in your Datadog platform.

2. Select a Host

3. Add a tag under the User tag section

4. The tag should look like this ```reflectiz.host.site:{site domain}```

5. If you want to add additional sites to a single host you can add more tags like this:

   * ```reflectiz.host.site.1:{site domain}```
   * ```reflectiz.host.site.2:{site domain}```
   * ```reflectiz.host.site.3:{site domain}```
   * etc...

In the example site domain is the domain of your site for example: ```example.com```.  
Once this is done all Metrics and Logs sent by the reflectiz integration for the site will be related to the Host


## Uninstallation

To uninstall the Reflectiz integration from Datadog:

1. **Go to the Integrations Section**:  
   Open your Datadog dashboard and navigate to the **Integrations** section.

2. **Locate the Reflectiz Integration**:  
   Find the **Reflectiz** tile in the list of installed integrations.

3. **Uninstall the Integration**:  
   Click on the integration tile and select **Uninstall Integration**.

4. **Delete the API Key (Optional but Recommended)**:  
   After uninstalling, remember to delete the API key associated with Reflectiz from your Datadog account. This ensures the integration no longer has access to your data.

This will fully remove the Reflectiz integration from your Datadog account.

## Data Collected

### Logs

The Reflectiz integration sends different types of logs to Datadog, each associated with a specific service. These logs provide detailed insights into scans, app risks, and domain risks, helping you monitor your website's security effectively.

#### 1. **Scan Logs**
- **Log Service Name**: `reflectiz.v1.scan`
- **Tags**:
  - `reflectiz.site`: Identifies the site being scanned.
  - `reflectiz.scan`: Give an identifier to the scan.
  - `reflectiz.scan.number`: Give an identifier to the scan as an integer for more filtering options.

These logs trigger each time a scan was run on a website.

#### 2. **Alert Logs**
- **Log Service Name**: `reflectiz.v1.alerts`
- **Tags**:
  - `reflectiz.site`: Identifies the site being scanned.
  - `reflectiz.scan`: Give an identifier to the scan.
  - `reflectiz.scan.number`: Give an identifier to the scan as an integer for more filtering options.
  - `reflectiz.app`: The app that is related to the alert (might be not provided).
  - `reflectiz.domain`: The domain that is related to the alert (might be not provided).

These logs highlights alerts triggered during the site's scan.


#### 3. **Rating Scan Logs**
- **Log Service Name**: `reflectiz.v1.scan`
- **Tags**:
  - `reflectiz.site`: Identifies the site being scanned.
  - `reflectiz.scan`: Give an identifier to the scan.
  - `reflectiz.scan.number`: Give an identifier to the scan as an integer for more filtering options.

These logs trigger each time a scan was run on a website and the ratings was calculated (useful to filter the rating data).

#### 4. **App Risks Logs**
- **Log Service Name**: `reflectiz.v1.rating.app.risks`
- **Tags**:
  - `reflectiz.site`: Indicates the site associated with the app.
  - `reflectiz.scan`: References the specific scan the log corresponds to.
  - `reflectiz.scan.number`: Give an identifier to the scan as an integer for more filtering options.
  - `reflectiz.app`: Identifies the application being assessed.

These logs highlight risks related to specific applications on your site, helping you pinpoint vulnerabilities.

#### 5. **Domain Risks Logs**
- **Log Service Name**: `reflectiz.v1.rating.domain.risks`
- **Tags**:
  - `reflectiz.site`: Indicates the site associated with the domain.
  - `reflectiz.scan`: References the specific scan the log corresponds to.
  - `reflectiz.scan.number`: Give an identifier to the scan as an integer for more filtering options.
  - `reflectiz.domain`: Identifies the domain being assessed.

These logs focus on risks related to domains, providing a clear picture of domain-specific vulnerabilities.

---

By analyzing these logs in your Datadog dashboard, you can gain actionable insights into the security posture of your sites, apps, and domains.

### Metrics

## Support
For support or feature requests, please contact Reflectiz through the following channels:

- Support email: support@reflectiz.com
- Sales email: inbound@reflectiz.com
- Website: reflectiz.com