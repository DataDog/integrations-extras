# AppOmni

## Overview

AppOmni Threat Detection Datadog Integration provides a single source to ingests and normalizes all your SaaS logs, and visualize events and alerts.

## Setup

**Log in to Datadog**
First Obtain a Datadog [API Key][1].  See the steps below:

Within Datadog navigate to **Organization settings** then click **API Keys**.
1. Click New Key
2. Provide a name for the API key
3. Click copy API key, and save this key for later.

**Create a Datadog AppOmni Destination**
**Log in to AppOmni**
1.  Navigate to **Threat Detection** and select **Destinations**.
2.  Click **Add New Destination**.
3.  Click the **Datadog Logs** card.
4.  Enter a **Name** and **Description** (optional).
5.  Ensure the following settings are checked:

-   **SSL Verification**
-   Select **Hash Original Field** to replace the original event field from the monitored service with a SHA256 hash of that event, thereby reducing event size.
-   Check **Gzip Compress Payloads** to reduce data size.

6.  Enter your **Datadog API Key**.
7.  Select your **Datadog site**. Identify which site you are on using [this table][2].
8.  Click **Save**.

## Uninstallation

**Log in to Datadog**
Within Datadog navigate to **Organization settings** then click **API Keys**.
1. Click Revoke Key for the API key you want to remove.

**Log in to AppOmni**
1.  Navigate to **Threat Detection** and select **Destinations**.
2.  Locate the **Datadog** destination and click on it.
3.  Click the **Configuration**
4.  Click **Delete**

## Support

Support can be reached by e-mail: support@appomni.com


[1]: https://docs.datadoghq.com/account_management/api-app-keys/
[2]: https://docs.datadoghq.com/getting_started/site/