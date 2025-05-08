# Pulse

## Overview

Pulse is a monitoring and optimization platform for Elasticsearch and OpenSearch clusters. It detects issues, tracks performance, delivers smart alerts, and recommendations to keep your search infrastructure healthy.

The integration ingests Pulse alerts as Datadog Events, enabling teams to centralize alert management, correlate issues with metrics and logs, and streamline incident response.

**Pulse shares the following data with Datadog**:

-   Alert title, severity, and description
-   Triggered and resolved timestamps
-   Cluster, nodes, and indices names

By connecting Pulse to Datadog, users gain full visibility into search performance and can respond to issues faster within existing workflows.

## Setup

1. In Pulse, navigate to the **Events & Alerts** tab in your cluster's page.

2. Click **Add destinations** and select **Datadog**.

3. Select your Datadog region from the dropdown.

4. Paste your Datadog API key.

5. Optionally, add tags separated by commas or spaces.

6. Select the alert severities you want to forward (Critical, Warning, and/or Informative).

7. Click **Send test alert** to verify setup.


## Uninstallation

1. In Pulse, navigate to the **Events & Alerts** tab in your cluster's page.

2. Scroll down to the Datadog card and click the trash icon in the bottom right corner. 

3. In Datadog, navigate to **Integrations**, select the Pulse tile, and click **Uninstall Integration**.

## Support

Need help? Contact [Pulse support][1] or open a support ticket directly via the Pulse platform.


[1]: mailto:info@pulse.support