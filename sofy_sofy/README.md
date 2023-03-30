# Sofy

## Overview

### What is Sofy 
SOFY is a no-code test automation platform that offers end-to-end testing from the CI/CD pipeline on real devices, making the testing process faster, more efficient, and more accessible than ever before. With SOFY, clients can automate the entire testing process, from test case planning to environment setup, and from reports to maintenance, without the need to write a single line of code. SOFY's intuitive interface sets it apart from other test automation platforms, allowing clients to achieve their software development goals with confidence.

### Sofy Datadog Dashboard
Integrating SOFY with Datadog allows you to gain even deeper insights into your testing process by visualizing key metrics and trends in the Datadog dashboard. With the ability to quickly and easily view how your device metrics are trending for each test case, you can identify potential issues early on and optimize your testing process for maximum efficiency. The Datadog dashboard provides real-time visibility into your SOFY test results, enabling you to monitor and analyze performance over time and make data-driven decisions to improve overall software quality. With this integration, you can take your testing and monitoring capabilities to the next level, ensuring that your applications perform flawlessly every time.

### Metrics

You can monitor the following device metrics:
* CPU Utilization
* Memory Utilization
* Load Time 
* Network


## Setup
Get set up in just a few steps:

1. Log in to [SOFY](https://portal.sofy.ai): Start by logging in to SOFY and navigating to the Account Setting page by selecting Account -> Account Setting from the left-hand navigation menu.

1. Connect Datadog: Once on the Account Setting page, select the [Integration tab](https://portal.sofy.ai/app/user-settings?selectedTab=integration) and locate the Datadog tile. Click the "Connect" button to begin the integration process.

1. Follow OAuth Steps: SOFY will prompt you to follow a series of OAuth steps to authorize the integration with Datadog. Follow these steps carefully, making sure to grant the necessary permissions to allow SOFY to send data to Datadog.

1. Visit Monitoring Tab: Once the integration is complete, navigate to the App Manager page by selecting it from the left-hand navigation menu. From there, click on the monitoring tab on the right-hand side of the page.

1. Enable Datadog Monitoring: Finally, enable Datadog monitoring for the selected app by toggling the appropriate switch. SOFY will now begin sending data to Datadog after each run in the selected app, allowing you to monitor and analyze the results in real time.


## Uninstallation
* Remove the Sofy API KEY from the Datadog Orginization Setting -> [API KEY](https://app.datadoghq.com/organization-settings/api-keys)

## Support
For support or feature requests, contact SOFY through the [following channel](https://support.sofy.ai/support/tickets/new)

## Further Reading
Additional helpful documentation, links, and articles:
* [Blog Post](https://sofy.ai/blog/)
* [Documentation](https://docs.sofy.ai)