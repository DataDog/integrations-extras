# Contrast Security ADR

## Overview

Contrast Security Application Detection & Response (ADR) for Datadog allows you to secure running applications like never before. Contrast Security ADR for Datadog provides timely actionable attack exploit events across the entire application portfolio. Contrast Security instrumented applications self-report the following about an attack – the attacker's IP address, method of attack, which applications, servers, frequency, volume, level of compromise, and more. In addition, Contrast Security can block these attacks in real time while also providing specific guidance to engineering teams on where applications were attacked and how threats can be remediated. 
Finally, Contrast Security's Log Enhancement capability extends this visibility into the inner workings of application and user behavior. Log Enhancers enable users to log anything in an application.


## Setup

## Step 1. Install the Contrast Security ADR Integration in Datadog

Navigate to https://www.datadoghq.com/integrations/contrast-security-adr and install the Integration.

## Step 2. Configure Contrast Security ADR to send Attack Events to Datadog

1.  In Contrast Security, go to the ****user menu**** and select ****Organization settings**** > ****Integrations****.

2.  Select the ****Datadog**** option under the ADR Integrations section.

3.  Under the Datadog fields, enter the URL and token information for your Datadog Log ingestion endpoint, as per: https://docs.datadoghq.com/api/latest/logs/#send-logs 

## Uninstallation

## Step 1. Disable sending events in Contrast Security ADR

1.  In Contrast Security, go to the ****user menu**** and select ****Organization settings**** > ****Integrations****.
2.  Select the ****Datadog**** option under the ADR Integrations section.
3.  Here you can either:\
    a. temporarily stop sending events (useful to stop sending events while retaining your URL and token configuration, or
    b. delete your configuration.

## Step 2. Uninstall the integration in Datadog
Navigate to https://www.datadoghq.com/integrations/contrast-security-adr and uninstall the Integration.



## Support

Contrast Security administrators wishing to troubleshoot the integration can check that:
-   Datadog tokens are correctly configured in Contrast Security Integration settings for the Contrast Security Organization,
-   Contrast Security ADR is enabled and attack events are successfully generated for the organisation.

Otherwise, Contrast Security Support can be contacted at <support@contrastsecurity.com>.


