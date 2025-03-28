# Hawkeye by NeuBird

## Overview

Hawkeye by NeuBird accelerates incident resolution by diagnosing incidents instantly and automating root cause analysis. Connecting Datadog and Hawkeye will allow Hawkeye to look for triggered Datadog Monitors and then autonomously investigate the root cause. Once investigation is complete, a link to the investigation analysis is added directly to the related Datadog incident, speeding-up resolution and reducing mean time to recovery.

## Setup

1.  In Datadog, navigate to **Integrations**, select the Hawkeye tile and click **Install Integration**.

2. Click **Connect Accounts** to start the authorization process. You will be redirected to Hawkeye to complete the setup.

3.  Once authorized, Hawkeye will begin sending investigation results to Datadog.


## Uninstallation

In Datadog, navigate to **Integrations**, select the Hawkeye tile and click **Uninstall Integration**.

- Once you uninstall this integration, any previous authorizations are revoked.

- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page][1].


## Support

Need help? Contact [NeuBird support][2].


[1]: https://app.datadoghq.com/organization-settings/api-keys?filter=Hawkeye
[2]: https://neubird.ai/neubird-support/