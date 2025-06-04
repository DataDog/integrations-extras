# Downdetector

## Overview

wndetector provides early alerting on service issues - often before internal monitoring tools.

This integration provides real-time Downdetector outage alerts as events in Datadog, enabling you to visualize and correlate service disruptions with your stack. It provides incident start and end notifications, along with details on the affected service, current measurements, baseline, top indicators, cities, and providers.

## Setup

1. In Datadog, navigate to **Integrations**, select the Downdetector tile, and click **Install Integration**.
2. Click **Connect Accounts** to start the authorization process. You will be redirected to Downdetector to complete the setup.
3. In Downdetector, navigate to **Alerts** > **Manage** to edit existing monitors or click **+** to create a new one.
5. In the monitor creation modal, select the newly created Datadog integration under the **Alert Settings** tab.


## Uninstallation

1. Navigate to **Alerts** > **Integrations** in Downdetector.
2. Click the trash icon next to the Datadog integration.
3. In Datadog, navigate to the [Downdetector][1] integration tile and click **Uninstall**. After you uninstall this integration, any previous authorizations are revoked.
4. Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page][2].

## Support

Contact support@downdetector.com for support requests.


[1]: /integrations/downdetector
[2]: /organization-settings/api-keys?filter=Downdetector
