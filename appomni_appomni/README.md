# AppOmni

## Overview

The AppOmni Threat Detection Datadog Integration centralizes and normalizes SaaS security logs, providing a unified view of events and alerts. This integration enhances visibility, enabling real-time monitoring and streamlined threat detection across your SaaS applications.

## Setup

### Create a Datadog API key

Create a Datadog [API Key][1].  See the steps below:

Within Datadog, navigate to **Organization settings**, then click **API Keys**.

1. Click **New Key**.

2. Provide a name for the API key.

3. Click **Copy API key**, and save this key for later.

### Create a Datadog AppOmni Destination

1.  Log into AppOmni

2. Navigate to **Threat Detection** and select **Destinations**.

3.  Click **Add New Destination**.

4.  Click the **Datadog Logs** card.

5.  Enter a **Name** and **Description** (optional).

6.  Ensure the following settings are checked:

**SSL Verification**

- Select **Hash Original Field** to replace the original event field from the monitored service with a SHA256 hash of that event, which reduces event size.

-   Check **Gzip Compress Payloads** to reduce data size.

7.  Enter your **Datadog API Key**.

8.  Select your **Datadog site**. Identify which site you are on using [the sites table][2].

9.  Click **Save**.


## Uninstallation

1. Within Datadog, navigate to **Organization settings**, then click **API Keys**.

2. Click **Revoke Key** for the API key you want to remove.

### In AppOmni

1. Navigate to **Threat Detection** and select **Destinations**.

2.  Locate the **Datadog** destination and click on it.

3.  Click **Configuration**

4.  Click **Delete**.


## Support

Contact <support@appomni.com> for support requests.


[1]: https://docs.datadoghq.com/account_management/api-app-keys/
[2]: https://docs.datadoghq.com/getting_started/site/