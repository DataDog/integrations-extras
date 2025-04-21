# Sofy

## Overview

Sofy is a no-code platform for creating automated tests on mobile apps. Users can integrate with their CI/CD pipelines to execute tests on real devices and view the results of their functional tests, along with performance metrics.

This integration provides deeper insight into your testing process by visualizing key metrics and trends such as load time, network, memory utilization, and CPU. The out-of-the-box dashboard provides real-time visibility into your Sofy test results, enabling you to monitor and analyze performance over time, and make data-driven decisions to improve overall software quality.

## Data Collected
### Metrics

See [metadata.csv][8] for the full list of metrics provided by this check.


## Setup
To set up the Sofy integration:

1. Go to your [Datadog Integrations page][1] and click on the Sofy tile.

2. Go to the **Configuration** tab and click **Install Integration** at the bottom.

3. Click **Connect Accounts** to redirect to the [Integration tab][3] under Account Settings in Sofy.

4. Log into [Sofy][2], then click the **Connect** button on the Datadog tile to begin the integration process.

5. Sofy will prompt you to follow a series of OAuth steps to authorize the integration with Datadog. Follow these steps carefully, making sure to grant the necessary permissions to allow Sofy to send data to Datadog.

6. Once the integration is complete, navigate to the App Manager page by selecting it from the left-hand menu. From there, click on the monitoring tab on the right-hand side of the page. Enable Datadog monitoring for the selected app by toggling the appropriate switch.

7. Sofy now starts sending data to Datadog after each run in the selected app, allowing you to monitor and analyze the results in real time.


## Uninstallation
* Ensure that all API keys associated with this integration have been disabled by searching for Sofy on the [API Keys management page][4] in Datadog.

## Support
Need help? Contact [Sofy support][5].

## Further Reading
Additional helpful documentation, links, and articles:
* [Monitor your mobile tests with Sofy's offering in the Datadog Marketplace][6]
* [Sofy Documentation][7]


[1]: /integrations
[2]: https://portal.sofy.ai
[3]: https://portal.sofy.ai/app/user-settings?selectedTab=integration
[4]: /organization-settings/api-keys?filter=Sofy
[5]: https://support.sofy.ai/support/tickets/new
[6]: https://www.datadoghq.com/blog/sofy-mobile-tests/
[7]: https://docs.sofy.ai
[8]: https://github.com/DataDog/integrations-extras/blob/master/sofy_sofy/metadata.csv
