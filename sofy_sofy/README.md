# Sofy

## Overview

### What is Sofy 
SOFY is a no-code test automation platform that offers end-to-end testing from the CI/CD pipeline on real devices, making the testing process faster, more efficient, and more accessible than ever before.

### Sofy Datadog Dashboard
Integrating SOFY with Datadog allows you to gain even deeper insights into your testing process by visualizing key metrics and trends in the Datadog dashboard.  The Datadog dashboard provides real-time visibility into your SOFY test results, enabling you to monitor and analyze performance over time and make data-driven decisions to improve overall software quality.

### Metrics

You can monitor the following device metrics:
* CPU Utilization
* Memory Utilization
* Load Time 
* Network


## Setup
Get set up in just a few steps:

1. Go to your [Datadog Integrations page](https://app.datadoghq.com/account/settings#integrations) and click on the SOFY tile. Then go to the **Configuration** tab and click **Install Integration** at the bottom.

1. Log in to [SOFY](https://portal.sofy.ai): Start by logging in to SOFY and navigating to the Account Setting page by selecting Account -> Account Setting from the left-hand navigation menu.

1. Connect Datadog: Once on the Account Setting page, select the [Integration tab](https://portal.sofy.ai/app/user-settings?selectedTab=integration) and locate the Datadog tile. Click the "Connect" button to begin the integration process.

1. Follow OAuth Steps: SOFY will prompt you to follow a series of OAuth steps to authorize the integration with Datadog. Follow these steps carefully, making sure to grant the necessary permissions to allow SOFY to send data to Datadog.

1. Visit Monitoring Tab: Once the integration is complete, navigate to the App Manager page by selecting it from the left-hand navigation menu. From there, click on the monitoring tab on the right-hand side of the page.

1. Enable Datadog Monitoring: Finally, enable Datadog monitoring for the selected app by toggling the appropriate switch. SOFY will now begin sending data to Datadog after each run in the selected app, allowing you to monitor and analyze the results in real time.


## Uninstallation
* Remove that all API keys associated with this integration have been disabled by searching for IsDown on the [API Keys management page](https://app.datadoghq.com/organization-settings/api-keys) in Datadog.

## Support
For support or feature requests, contact SOFY through the [following channel](https://support.sofy.ai/support/tickets/new)

## Further Reading
Additional helpful documentation, links, and articles:
* [Blog Post](https://sofy.ai/blog/)
* [Documentation](https://docs.sofy.ai)