# Jamf Protect

## Overview
[Jamf Protect][1] is a comprehensive security solution designed specifically for Apple endpoints, including macOS, iOS and iPadOS endpoints and other supported platforms. Jamf Protect enhances Apple's built-in security features and provides real-time detection of malicious applications, scripts, and user activities. 

Jamf Protect not only detects known malware, adware, but also prevents unknown threats and blocks command and control traffic and risky domains. Furthermore, it provides granular insights into endpoint activity, ensuring endpoint health and compliance, and supports incident response with automated workflows. This integration will collect logs from Jamf Protect events which can be analyzed using Datadog. This integration monitors Jamf Protect logs for both macOS Security and Jamf Security Cloud.

## Setup

### Installation

Navigate to the [Integrations page][6] and search for the "Jamf Protect" tile. 


### Determine your Datadog Intake URL

Using the [Datadog API Logs documentation][7], determine what your intake URL is by selecting your [Datadog Site][8] on the top right corner. 


### macOS Security Portal
1.  Click **Actions**.
2.  Click **Create Actions**.
3.  **Name:** Datadog.
4.  Click **Remote Alert Collection Endpoints**.

    a.  **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=alerts`

    b.  Set **Min Severity & Max Severity:**

    c.  Click **+ Add HTTP Header**. 
    ```
    i.  Name: DD-API-KEY
    ii.  Value: <API_Key>
    ```
            
    d.  Click **+ Add HTTP Header**.
    ```
    i.  Name: DD-APPLICATION-KEY
    ii. Value: <APPLICATION_KEY>
    ```

5.  Click **+ Unified Logs Collection Endpoints**.

    a.  **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=unifiedlogs`

    b.  Click + **Add HTTP Header**.
    ```
    i.  Name: DD-API-KEY
    ii. Value: <API_Key>
    ```

    c.  Click **+ Add HTTP Header**.
    ```
    i.  Name: DD-APPLICATION-KEY
    ii. Value: <APPLICATION_KEY>
    ```

6.  Click **+ Telemetry Collection Endpoints**.

    a.  **URL:** `https://${DATADOG_INTAKE_URL}/api/v2/logs?ddsource=jamfprotect&service=telemetry`

    b.  Click **+ Add HTTP Header**.
    ```
    i.  Name: DD-API-KEY
    ii. Value: <API_Key>
    ```

    c.  Click **+ Add HTTP Header**.
    ```
    i.  Name: DD-APPLICATION-KEY
    ii. Value: <APPLICATION_KEY>
    ```

7.  Click **Save**.


### Jamf Security Cloud


1.  Click **Integrations** in the Threat Events Stream.
2.  Click **Data Streams**.
3.  Click **New Configuration**.
4.  Select **Threat Events**.
    a.  Select **Generic HTTP**.
5.  Click **Continue**.

    a.  **Configuration** **Name:** Datadog (Threat)

    b.  **Protocol:** **HTTPS**

    c.  **Server** **Hostname/IP:** `${DATADOG_INTAKE_URL}`

    d.  **Port:** **443**

    e.  **Endpoint:** `api/v2/logs?ddsource=jamfprotect&service=threatevents`
    
    f.  **Additional Headers:**

    i.  **Header Name:** DD-API-KEY
        
6.  Click **Create option "DD-API-KEY"**.
    ```
    i.  **Header Value:** <API_Key>
    ii.  **Header Name**: DD-APPLICATION-KEY
    ```
7.  Click **Create option "DD-APPLICATION-KEY"**.
    ```
    iii.  **Header Value:** <APPLICATION_KEY>
    ```
    1.  Click **Test Configuration**.

    2.  If successful, click **Create Configuration**.

### Network Traffic Stream
1.  Click **Integrations**.
2.  Click **Data Streams**.
3.  Click **New Configuration**.
4.  Select **Threat Events**.

    a.  Select **Generic HTTP**.

5.  Click **Continue**.
    a.  **Configuration** **Name:** Datadog (Threat)

    b.  **Protocol:** **HTTPS**

    c.  **Server** **Hostname/IP:** `${DATADOG_INTAKE_URL}`

    d.  **Port:** **443**

    e.  **Endpoint:** `api/v2/logs?ddsource=jamfprotect&service=networktraffic`

    1. **Additional Headers:**

        i.  **Header Name:** DD-API-KEY

        1.  Click **Create option "DD-API-KEY"**.

        ii.  **Header Value:** <API_Key>

           i. Header Name: DD-APPLICATION-KEY

        iv.  Click **Create option "DD-APPLICATION-KEY"**.

           i. Header Value: <APPLICATION_KEY>

6.  Click **Test Configuration**.
7.  If successful, click **Create Configuration**.


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

[1]: https://www.jamf.com/products/jamf-protect/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/
[4]: https://learn.jamf.com/bundle/jamf-protect-documentation/page/Audit_Logs.html
[5]: https://app.datadoghq.com/logs
[6]: https://app.datadoghq.com/integrations
[7]: https://docs.datadoghq.com/api/latest/logs/#send-logs
[8]: https://docs.datadoghq.com/getting_started/site/
