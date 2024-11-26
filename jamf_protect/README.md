# Jamf Protect

## Overview
[Jamf Protect][1] is a comprehensive security solution designed specifically for Apple endpoints, including macOS, iOS and iPadOS endpoints and other supported platforms. Jamf Protect enhances Apple's built-in security features and provides real-time detection of malicious applications, scripts, and user activities. 

Jamf Protect not only detects known malware, adware, but also prevents unknown threats and blocks command and control traffic and risky domains. Furthermore, it provides granular insights into endpoint activity, ensuring endpoint health and compliance, and supports incident response with automated workflows. This integration will collect logs from Jamf Protect events which can be analyzed using Datadog. This integration monitors Jamf Protect logs for both macOS Security and Jamf Security Cloud.

## Setup

### Prerequisites

- Datadog intake URL. Use the [Datadog API Logs documentation][7] and select your Datadog Site at the top of the page.
- Your [Datadog API and App keys][10].

### Installation

Navigate to the [Integrations page][6] and search for the "Jamf Protect" tile. 

### macOS Security Portal
1. In Jamf Protect, click **Actions**.
2.  Click **Create Actions**.
3.  In the *Action Config Name* field, enter a name (such as `Datadog`).
4.  (Optional) To collect alerts, click **Remote Alert Collection Endpoints** and add the following:

    a. **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=alerts`

    b. Set **Min Severity & Max Severity**.

    c. Click **+ Add HTTP Header** twice and add the following HTML header fields: 
      ```
      Name: DD-API-KEY
      Value: <API_Key>
      ```
      ```
      Name: DD-APPLICATION-KEY
      Value: <APPLICATION_KEY>
      ```

5. (Optional) To collect unified logs, click **+ Unified Logs Collection Endpoints** and add the following.

    a. **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=unifiedlogs`

    b. Click **+ Add HTTP Header** twice and add the following HTML header fields.
      ```
      Name: DD-API-KEY
      Value: <API_Key>
      ```
      ```
      Name: DD-APPLICATION-KEY
      Value: <APPLICATION_KEY>
      ```

6. (Optional) To collect telemetry data, click **+ Telemetry Collection Endpoints**.

    a.  **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=telemetry`

    b.  Click **+ Add HTTP Header** twice and add the following HTML header fields.
      ```
      Name: DD-API-KEY
      Value: <API_Key>
      ```
      ```
      Name: DD-APPLICATION-KEY
      Value: <APPLICATION_KEY>
      ```

7. Click **Save**.

### Update your plan to use configured Actions

1. Click **Plans**.
1. Find the plan assigned to devices.
1. Click **Edit** next to the name of the plan.
1. Select the Action from the *Action Configuration* dropdown menu. This is the Action config name that contains the Datadog configuration.
1. Click **Save**.

### (Optional) Jamf Security Cloud

1.  Click **Integrations** in the Threat Events Stream.
2.  Click **Data Streams**.
3.  Click **New Configuration**.
4.  Select **Threat Events**.
5.  Select **Generic HTTP**.
6.  Click **Continue**.
    | **Configuration**        | **Details**                         |
    |--------------------------|-------------------------------------|
    | **Name**                 | Datadog (Threat)                    |
    | **Protocol**             | HTTPS                               |
    | **Server Hostname/IP**   | `${DATADOG_INTAKE_URL}`             |
    | **Port**                 | 443                                 |
    | **Endpoint**             | `api/v2/logs?ddsource=jamfprotect&` |
        
7.  Click **Create option "DD-API-KEY"**.
    ```
    Header Value: <API_Key>
    Header Name: DD-APPLICATION-KEY
    ```
8.  Click **Create option "DD-APPLICATION-KEY"**.
    ```
    Header Value: <APPLICATION_KEY>
    ```
9.  Click **Test Configuration**.

10.  If successful, click **Create Configuration**.

### (Optional) Network Traffic Stream

1.  Click **Integrations**.
2.  Click **Data Streams**.
3.  Click **New Configuration**.
4.  Select **Threat Events**.

5. Select **Generic HTTP**.

6.  Click **Continue**.
    a.  **Configuration Name:** Datadog (Threat)

    b.  **Protocol:** **HTTPS**

    c.  **Server** **Hostname/IP:** `${DATADOG_INTAKE_URL}`

    d.  **Port:** **443**

    e.  **Endpoint:** `api/v2/logs?ddsource=jamfprotect&service=networktraffic`

    f. **Additional Headers:**

        i.  **Header Name:** DD-API-KEY

        1.  Click **Create option "DD-API-KEY"**.

        ii.  **Header Value:** <API_Key>

           i. Header Name: DD-APPLICATION-KEY

        iv.  Click **Create option "DD-APPLICATION-KEY"**.

           i. Header Value: <APPLICATION_KEY>

7.  Click **Test Configuration**.
8.  If successful, click **Create Configuration**.

### Validation

Navigate to the [Logs Explorer][5] and search for `source:jamfprotect` to validate you are receiving logs.

## Data Collected

### Logs

The Jamf Protect integration allows you to send [Jamf Audit Logs][4] to Datadog.

### Metrics

Jamf Protect does not include any metrics.

### Service Checks

Jamf Protect does not include any service checks.

### Events

Jamf Protect does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

## Further Reading

Additional helpful documentation, links, and articles:

[Jamf Documentation Integrating Datadog with Jamf Protect][9]

[1]: https://www.jamf.com/products/jamf-protect/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/
[4]: https://learn.jamf.com/bundle/jamf-protect-documentation/page/Audit_Logs.html
[5]: https://app.datadoghq.com/logs
[6]: https://app.datadoghq.com/integrations
[7]: https://docs.datadoghq.com/api/latest/logs/#send-logs
[8]: https://docs.datadoghq.com/getting_started/site/
[9]: https://learn.jamf.com/en-US/bundle/jamf-protect-documentation/page/SecurityIntegration_Datadog.html
[10]: https://docs.datadoghq.com/account_management/api-app-keys/