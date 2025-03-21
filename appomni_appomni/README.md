# AppOmni

## Overview

**AppOmni** is a leading SaaS security platform that provides deep visibility, monitoring, and control over enterprise SaaS applications. It helps organizations secure their data by detecting misconfigurations, unauthorized access, and potential threats in SaaS cloud applications.

The **AppOmni integration** centralizes your SaaS security logs within Datadog, giving you a unified view of security events and alerts. AppOmni normalizes security events across different SaaS applications, ensuring consistency in log structure and making it easier to correlate activities across platforms.

AppOmni generates alerts based on multiple detection methods:

-   **User and Entity Behavior Analytics (UEBA):** Detects anomalies in user activity by establishing baselines and identifying deviations that may indicate compromised accounts or insider threats.
-   **Threshold-based Alerts:** Triggers notifications when predefined limits (e.g., excessive failed login attempts, high-volume data exports) are exceeded.
-   **Sequence-based Detection:** Identifies complex attack patterns by analyzing the order and relationship of events, such as privilege escalation followed by sensitive data access.

By integrating with Datadog, these insights enable security teams to detect, investigate, and respond to threats in real time, improving the overall security posture of their SaaS environments.

## Setup

### Create a Datadog API key

Create a Datadog [API Key][1].  See the steps below:

2. Log into Datadog.
3. Navigate to **Organization settings**, then click **API Keys**.
4. Click **New Key**.
5. Provide a name for the API key.
6. Click **Copy API key**, and save this key for later.

### Create a Datadog AppOmni Destination

1. Log into AppOmni.
2. Navigate to **Threat Detection** and select **Destinations**.
3. Click **Add New Destination**.
4. Click the **Datadog Logs** card.
5. Enter a **Name** and **Description** (optional).
6. Ensure the following settings are checked:  **SSL Verification**, **Hash Original Field**, **Gzip Compress Payloads**.
7. Enter your **Datadog API Key**.
8. Select your **Datadog site**. Identify which site you are on using [the sites table][2].
9. Click **Save**.


## Uninstallation

1. Within Datadog, navigate to **Organization settings**, then click **API Keys**.

2. Click **Revoke Key** for the API key you want to remove.

### In AppOmni

1. Navigate to **Threat Detection** and select **Destinations**.

2. Locate the **Datadog** destination and click on it.

3. Click **Configuration**.

4. Click **Delete**.


## Support

Contact support@appomni.com for support requests.


[1]: https://docs.datadoghq.com/account_management/api-app-keys/
[2]: https://docs.datadoghq.com/getting_started/site/