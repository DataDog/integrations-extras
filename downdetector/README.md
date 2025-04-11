# Downdetector

## Overview

Downdetector provides early alerting on service issues - often before internal monitoring tools.

This integration provides real-time Downdetector outage alerts as events in Datadog, enabling you to visualize and correlate service disruptions with your stack. It provides incident start and end notifications, along with details on the affected service, current measurements, baseline, top indicators, cities, and providers.

## Setup

1. Log in to your [Downdetector account][1] or [sign up][2].
2. Navigate to **Alerts** > **Integrations** and click the **+** in the top right.
3. Select **Add Datadog** and complete the authorization in Datadog. Once authorized, you'll be redirected back to Downdetector.
4. Navigate to **Alerts** > **Manage** to edit existing monitors or click **+** to create a new one.
5. In the monitor creation modal, select the newly created Datadog integration under the **Alert Settings** tab.


## Uninstallation

1. Navigate to **Alerts** > **Integrations** in Downdetector.
2. Click the trash icon next to the Datadog integration.
3. In Datadog, navigate to the [Downdetector][3] integration tile and click **Uninstall**. After you uninstall this integration, any previous authorizations are revoked.
4. Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page][4].

## Support

Contact support@downdetector.com for support requests.


[1]: https://enterprise.downdetector.com/
[2]: <https://downdetector.com/for-business/>
[3]: https://app.datadoghq.com/integrations/downdetector
[4]: https://app.datadoghq.com/organization-settings/api-keys?filter=Downdetector