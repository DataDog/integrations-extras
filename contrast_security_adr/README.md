# Contrast Security ADR

## Overview

This is a new line.

Contrast Security Application Detection and Response (ADR) platform provides real-time visibility and protection against attacks targeting applications and APIs by embedding security directly within application runtimes. 

Integrating Contrast Security ADR with Datadog enhances threat detection by forwarding detailed application-layer attack events as logs. This enables security teams to correlate application-level threats with infrastructure and network activity, accelerating triage and investigation. It also provides actionable context with rich details such as attack methods, payloads, TTPs, targeted applications, affected servers, and levels of compromise.

## Setup

1. In Datadog, navigate to **Integrations**, select the Contrast Security ADR tile, and click **Install Integration**.

2. In Contrast Security, navigate to the user menu, select **Organization settings**, and click **Integrations**.

3. Select **Datadog**.

4. Enter your Datadog site URL and paste your Datadog API Key.


## Uninstallation

1. In Contrast Security, navigate to the user menu, select **Organization settings**, and click **Integrations**.
2. Select **Datadog**.
3. Click **Delete** to permanently remove the connection.
   > **Note**: You can temporarily disable the integration and maintain the configuration by clicking "Disable".
4. In Datadog, navigate to **Integrations**, select the Contrast Security ADR tile, and click **Uninstall Integration**.


## Support

Need help? Contact [Contrast Security support][1].


[1]: mailto:support@contrastsecurity.com
