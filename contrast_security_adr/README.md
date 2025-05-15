# Contrast Security ADR

## Overview

Contrast Security Application Detection and Response (ADR) provides real-time visibility and protection against attacks targeting applications and APIs by embedding security directly within application runtimes. Integrating Contrast Security ADR with Datadog enhances threat detection and response by sending detailed application-layer attack events as logs into Datadog. This provides security teams with visibility into application runtimes, correlating application-level threats with infrastructure and network events for faster and more accurate incident triage and investigation. The Contrast Security-maintained pipeline provides accurate parsing and mapping of Contrast Security ADR data with the Datadog Cloud SIEM data model, including the attack detail, payload, and TTPs, targeted applications, servers, and level of compromise.

## Setup

1. In Datadog, navigate to **Integrations**, select the Contrast Security ADR tile, and click **Install Integration**.

2. In Contrast Security, navigate to the user menu, select **Organization settings**, and click **Integrations**.

3. Select **Datadog**.

4. Enter your Datadog site URL and paste your Datadog API Key.


## Uninstallation

1. In Contrast Security, navigate to the user menu, select **Organization settings**, and click **Integrations**.
2. Select **Datadog**.
3. Click **Delete** to permanently remove the connection.\
   > **Note**: You can temporarily disable the integration and maintain the configuration by clicking "Disable".
4. In Datadog, navigate to **Integrations**, select the Contrast Security ADR tile, and click **Uninstall Integration**.


## Support

Need help? Contact [Contrast Security support][1].


[1]: support@contrastsecurity.com